#!/usr/bin/env python3
"""Boot the exact vanilla server and test real mcfunctions over loopback RCON.

Never point this tool at a real world. It owns an isolated temporary world, accepts
Minecraft's EULA only with --accept-eula, and exports logs/JUnit, not server binaries.
"""
from __future__ import annotations
import argparse
from contextlib import suppress
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import traceback
import urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.build import ROOT, build  # noqa: E402

MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"


def get_json(url: str) -> dict:
    if not url.startswith("https://"):
        raise ValueError("Download URLs must use HTTPS")
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def download_server(version: str, cache: Path) -> Path:
    manifest = get_json(MANIFEST)
    entry = next((item for item in manifest["versions"] if item["id"] == version), None)
    if entry is None:
        raise RuntimeError(f"Exact target {version} is absent from Mojang's manifest; refusing fallback")
    info = get_json(entry["url"])
    if info["id"] != version:
        raise RuntimeError("Version metadata mismatch")
    server = info["downloads"]["server"]
    cache.mkdir(parents=True, exist_ok=True)
    jar = cache / f"server-{version}.jar"
    expected = server["sha1"]
    if jar.exists() and hashlib.sha1(jar.read_bytes()).hexdigest() != expected:
        jar.unlink()
    if not jar.exists():
        request = urllib.request.Request(server["url"], headers={"User-Agent": "NPCraft-CI/0.1"})
        with urllib.request.urlopen(request, timeout=90) as source, jar.with_suffix(".part").open("wb") as target:
            shutil.copyfileobj(source, target)
        jar.with_suffix(".part").replace(jar)
    if jar.stat().st_size != server["size"] or hashlib.sha1(jar.read_bytes()).hexdigest() != expected:
        jar.unlink(missing_ok=True)
        raise RuntimeError("Official server download failed size/SHA-1 verification")
    return jar


class Rcon:
    """Minimal bounded Source RCON transport; no third-party Python dependency."""
    def __init__(self, port: int, password: str):
        self.socket = socket.create_connection(("127.0.0.1", port), timeout=5)
        self.socket.settimeout(15)
        self.sequence = 0
        self.request(password, kind=3)

    def _read_exactly(self, size: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < size:
            part = self.socket.recv(size - len(chunks))
            if not part:
                raise ConnectionError("RCON connection closed")
            chunks.extend(part)
        return bytes(chunks)

    def request(self, text: str, kind: int = 2) -> str:
        self.sequence += 1
        payload = struct.pack("<ii", self.sequence, kind) + text.encode("utf-8") + b"\0\0"
        self.socket.sendall(struct.pack("<i", len(payload)) + payload)
        for _ in range(4):
            length = struct.unpack("<i", self._read_exactly(4))[0]
            if not 10 <= length <= 1024 * 1024:
                raise ConnectionError(f"Invalid RCON packet size {length}")
            packet = self._read_exactly(length)
            request_id, _ = struct.unpack("<ii", packet[:8])
            if request_id == -1:
                raise PermissionError("RCON authentication failed")
            if request_id == self.sequence:
                return packet[8:-2].decode("utf-8")
        raise ConnectionError("RCON response ID mismatch")

    def close(self) -> None:
        self.socket.close()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class Server:
    def __init__(self, work: Path, jar: Path, archive: Path, reports: Path):
        self.work, self.jar, self.reports = work, jar, reports
        self.process: subprocess.Popen | None = None
        self.rcon: Rcon | None = None
        self.console = None
        self.password = secrets.token_hex(24)
        self.port = free_port()
        self.launch = 0
        (work / "world/datapacks").mkdir(parents=True)
        shutil.copy2(archive, work / "world/datapacks" / archive.name)
        (work / "eula.txt").write_text("eula=true\n")
        properties = {
            "server-ip": "127.0.0.1", "server-port": free_port(),
            "enable-rcon": "true", "rcon.port": self.port, "rcon.password": self.password,
            "online-mode": "false", "white-list": "false", "enable-status": "false",
            "level-name": "world", "level-type": "minecraft:flat",
            "generator-settings": '{"biome":"minecraft:plains","layers":[{"block":"minecraft:bedrock","height":1},{"block":"minecraft:dirt","height":2},{"block":"minecraft:grass_block","height":1}]}',
            "view-distance": 3, "simulation-distance": 3, "spawn-protection": 0,
            "max-players": 1, "max-tick-time": 60000, "pause-when-empty-seconds": -1,
            "broadcast-rcon-to-ops": "false", "spawn-monsters": "false",
        }
        (work / "server.properties").write_text("".join(f"{key}={value}\n" for key, value in properties.items()))

    def start(self) -> None:
        self.launch += 1
        self.console = (self.reports / f"server-{self.launch}.log").open("w", encoding="utf-8")
        self.process = subprocess.Popen(["java", "-Xms512M", "-Xmx1536M", "-jar", str(self.jar), "nogui"],
                                        cwd=self.work, stdin=subprocess.DEVNULL,
                                        stdout=self.console, stderr=subprocess.STDOUT)
        deadline = time.monotonic() + 180
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError(f"Server exited with {self.process.returncode}; inspect server-{self.launch}.log")
            try:
                self.rcon = Rcon(self.port, self.password)
                response = self.rcon.request("data get storage npcraft:meta version")
                if json.loads((ROOT / "project.json").read_text())["version"] in response:
                    self.assert_clean_logs()
                    return
                self.rcon.close()
            except (OSError, ConnectionError):
                pass
            time.sleep(1)
        raise TimeoutError("Vanilla server did not become ready in 180 seconds")

    def command(self, command: str) -> str:
        if self.rcon is None:
            raise RuntimeError("Server is not connected")
        response = self.rcon.request(command)
        # Commands intentionally testing a false condition may return failure; syntax errors may not.
        if any(fragment in response for fragment in ("Unknown or incomplete command", "Incorrect argument", "Unknown function", "Failed to instantiate macro")):
            raise AssertionError(f"Command failed: {command}\n{response}")
        return response

    def expect(self, condition: str, truth: bool = True) -> None:
        self.command(f"execute store success score #assert np.tmp run execute {condition}")
        answer = self.command("scoreboard players get #assert np.tmp")
        match = re.search(r"has (-?\d+) \[np\.tmp\]", answer)
        if not match or (int(match.group(1)) > 0) != truth:
            diagnostics = []
            for query in (f"data get entity {BOT} data", f"data get entity {BOT} Pos",
                          f"scoreboard players list {BOT}", "scoreboard players list #y",
                          "scoreboard players list #goal_y", "scoreboard players list #range",
                          "scoreboard players list #arrived", "scoreboard players list #found",
                          "scoreboard players list #nodes", "scoreboard players list #visible"):
                with suppress(Exception):
                    diagnostics.append(f"{query}: {self.command(query)}")
            raise AssertionError(f"Expected {condition!r} to be {truth}; response: {answer}\n" + "\n".join(diagnostics))

    def assert_clean_logs(self) -> None:
        if self.console:
            self.console.flush()
        text = "\n".join(path.read_text(errors="replace") for path in self.reports.glob("server-*.log"))
        bad = [line for line in text.splitlines() if re.search(
            r"Failed to load function|Failed to parse|Couldn't load tag|Couldn't parse|Failed to execute function|Failed to instantiate macro|Errors in currently selected data packs|Unknown registry key|Unbound values in registry|Serialization errors", line)]
        if bad:
            raise AssertionError("Minecraft rejected datapack resources:\n" + "\n".join(bad[:30]))

    def stop(self) -> None:
        if self.process is None:
            return
        if self.process.poll() is None and self.rcon is not None:
            with suppress(Exception):
                self.rcon.request("stop")
        if self.rcon:
            self.rcon.close()
            self.rcon = None
        try:
            self.process.wait(timeout=35)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=10)
        if self.console:
            self.console.close()
            self.console = None


BOT = '@e[type=minecraft:marker,tag=npcraft.test,limit=1]'
AS = f"execute as {BOT} at @s run "
TOOL = '{id:"minecraft:iron_axe",count:1,components:{"minecraft:damage":0}}'


def fixture(server: Server) -> None:
    c = server.command
    c("function npcraft:admin/pause")
    c("forceload add -16 -16 32 32")  # Test world only; prohibited in distributed functions.
    deadline = time.monotonic() + 20
    while time.monotonic() < deadline:
        try:
            server.expect("if loaded -8 64 -8 if loaded -8 64 8 if loaded 16 64 -8 if loaded 16 64 8")
            break
        except AssertionError:
            time.sleep(0.2)
    else:
        raise TimeoutError("Test chunks did not load")
    c("execute as @e[type=minecraft:mannequin,tag=npcraft.body] run function npcraft:bot/retire")
    for tag in ("npcraft.bot", "npcraft.nav"):
        c(f"kill @e[tag={tag}]")
    c("kill @e[type=minecraft:item]")
    c("fill -8 63 -8 16 63 8 minecraft:stone")
    c("fill -8 64 -8 16 69 8 minecraft:air")
    c('data modify storage npcraft:state queue set value []')
    c('summon minecraft:marker 0.5 64 0.5 {Tags:["npcraft.bot","npcraft.test"],data:{schema:1,id:9001,owner:1,owner_uuid:[I;0,0,0,1],scan:0,scanned:0,home:{x:0,y:64,z:0},plot:{x:0,y:64,z:0},dest:{x:4,y:64,z:0,range:0},storage:{x:0,y:64,z:1},tool:'+TOOL+'}}')
    for obj, value in (("np.id",9001),("np.owner",1),("np.mode",0),("np.status",0),("np.dig",0),("np.next",0),("np.harvest",0)):
        c(f"scoreboard players set {BOT} {obj} {value}")
    c("scoreboard players set #now np.sys 1000")
    c(AS + "function npcraft:bot/sync with entity @s data")


def set_target(s: Server, x: int = 1, y: int = 64, z: int = 0, kind: str = "oak_log") -> None:
    s.command(f'setblock {x} {y} {z} minecraft:{kind}')
    s.command(AS + f'data modify entity @s data.target set value {{x:{x},y:{y},z:{z},kind:"minecraft:{kind}"}}')


def test_native_body(s: Server) -> None:
    s.expect('if entity @e[type=minecraft:mannequin,tag=npcraft.body,scores={np.id=9001},nbt={Invulnerable:1b}]')
    s.expect('if items entity @e[tag=npcraft.body,limit=1] weapon.mainhand minecraft:iron_axe')


def test_reload(s: Server) -> None:
    s.command("scoreboard players set #next np.sys 37")
    s.command('data modify storage npcraft:state queue set value [{id:9001}]')
    s.command("reload")
    time.sleep(2)
    s.expect("if score #next np.sys matches 37")
    s.expect('if data storage npcraft:state queue[{id:9001}]')
    s.expect('if score #enabled np.sys matches 0')
    s.assert_clean_logs()


def test_wall_detour(s: Server) -> None:
    s.command("fill 2 64 -1 2 66 1 minecraft:stone")
    for _ in range(14):
        s.command(AS + "function npcraft:nav/plan")
    s.expect(f'if data entity {BOT} {{Pos:[4.5d,64.0d,0.5d]}}')
    s.expect("if block 2 64 0 minecraft:stone")
    s.expect("if entity @e[tag=npcraft.nav]", False)


def test_far_goal(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.dest set value {x:12,y:64,z:0,range:0}')
    for _ in range(16):
        s.command(AS + "function npcraft:nav/plan")
    s.expect(f'if data entity {BOT} {{Pos:[12.5d,64.0d,0.5d]}}')


def test_gap(s: Server) -> None:
    s.command("fill 1 63 -8 1 63 8 minecraft:air")
    s.command(AS + 'data modify entity @s data.dest set value {x:2,y:64,z:0,range:0}')
    s.command(AS + "function npcraft:nav/plan")
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,64.0d,0.5d]}}')
    s.expect(f"if score {BOT} np.status matches 4")
    s.expect("if block 1 63 0 minecraft:air")


def test_height_and_hazard(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.dest.y set value 65')
    s.command(AS + "function npcraft:nav/plan")
    s.expect(f'if data entity {BOT} {{Pos:[0.5d,64.0d,0.5d]}}')
    s.command("setblock 0 64 0 minecraft:lava")
    s.command(AS + "execute store result score #safe np.tmp run function npcraft:nav/cell_safe")
    s.expect("if score #safe np.tmp matches 0")
    s.command("execute positioned 10000 64 10000 store result score #safe np.tmp run function npcraft:nav/cell_safe")
    s.expect("if score #safe np.tmp matches 0")
    s.expect("if loaded 10000 64 10000", False)


def test_scan_and_harvest(s: Server) -> None:
    s.command("setblock 1 64 0 minecraft:oak_log")
    for _ in range(5):
        s.command(AS + "function npcraft:work/scan")
    s.expect(f'if data entity {BOT} data.target{{x:1,y:64,z:0,kind:"minecraft:oak_log"}}')
    s.command(AS + "function npcraft:work/tick")
    s.expect("if block 1 64 0 minecraft:oak_log")  # Not instant mining.
    s.command("scoreboard players set #now np.sys 1025")
    s.command(AS + "function npcraft:work/tick")
    s.expect("if block 1 64 0 minecraft:air")
    s.expect(f'if data entity {BOT} data.cargo{{id:"minecraft:oak_log",count:1}}')
    s.expect(f'if data entity {BOT} data.tool.components{{"minecraft:damage":1}}')
    s.expect(f"if score {BOT} np.harvest matches 1")


def test_stale_target(s: Server) -> None:
    set_target(s)
    s.command("setblock 1 64 0 minecraft:stone")
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect(f"if data entity {BOT} data.cargo", False)
    s.expect("if block 1 64 0 minecraft:stone")
    s.expect(f'if data entity {BOT} data.tool.components{{"minecraft:damage":0}}')


def test_plot_bounds(s: Server) -> None:
    set_target(s, x=4)
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect("if block 4 64 0 minecraft:oak_log")
    s.expect(f"if data entity {BOT} data.cargo", False)
    s.command(AS + 'data modify entity @s data.plot set value {x:-4,y:64,z:-4}')
    set_target(s, x=-7, z=-7)
    s.command(AS + "execute store result score #bounds np.tmp run function npcraft:work/in_bounds")
    s.expect("if score #bounds np.tmp matches 1")
    s.command(AS + 'data modify entity @s data.target.x set value -8')
    s.command(AS + "execute store result score #bounds np.tmp run function npcraft:work/in_bounds")
    s.expect("if score #bounds np.tmp matches 0")


def test_missing_tool(s: Server) -> None:
    set_target(s)
    s.command(AS + "data remove entity @s data.tool")
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect("if block 1 64 0 minecraft:oak_log")
    s.expect(f"if data entity {BOT} data.cargo", False)


def test_full_cargo(s: Server) -> None:
    set_target(s)
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:64}')
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect("if block 1 64 0 minecraft:oak_log")
    s.expect(f"if data entity {BOT} data.cargo{{count:64}}")


def test_stack_and_type(s: Server) -> None:
    set_target(s)
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:63}')
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect(f"if data entity {BOT} data.cargo{{count:64}}")
    s.command(AS + 'data modify entity @s data.cargo.count set value 1')
    set_target(s, kind="birch_log")
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect("if block 1 64 0 minecraft:birch_log")
    s.expect(f'if data entity {BOT} data.cargo{{id:"minecraft:oak_log",count:1}}')


def test_line_of_sight(s: Server) -> None:
    set_target(s, x=2)
    s.command("fill 1 64 0 1 66 0 minecraft:stone")
    s.command("scoreboard players set #now np.sys 2000")
    s.command(f"scoreboard players set {BOT} np.dig 1")
    s.command(AS + "function npcraft:work/harvest")
    s.expect("if block 2 64 0 minecraft:oak_log")
    s.expect(f"if score {BOT} np.status matches 9")


def test_full_barrel_and_transfer(s: Server) -> None:
    s.command("setblock 0 64 1 minecraft:barrel")
    for slot in range(27):
        s.command(f"item replace block 0 64 1 container.{slot} with minecraft:stone 64")
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:64}')
    s.command(AS + "function npcraft:work/deposit")
    s.expect(f"if score {BOT} np.status matches 5")
    s.expect(f"if data entity {BOT} data.cargo{{count:64}}")
    s.command("item replace block 0 64 1 container.9 with minecraft:air")
    s.command(AS + "function npcraft:work/deposit")
    s.expect("if items block 0 64 1 container.9 minecraft:oak_log")
    s.expect('if data block 0 64 1 Items[{Slot:9b,count:64}]')
    s.expect("if items block 0 64 1 container.0 minecraft:stone")
    s.expect(f"if data entity {BOT} data.cargo", False)
    s.command(AS + "function npcraft:work/deposit")
    s.expect('if data block 0 64 1 Items[{Slot:9b,count:64}]')


def test_missing_barrel(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:7}')
    s.command(AS + "function npcraft:work/deposit")
    s.expect(f"if data entity {BOT} data.cargo{{count:7}}")
    s.expect(f"if score {BOT} np.status matches 8")


def test_axe_break(s: Server) -> None:
    set_target(s)
    s.command(AS + 'data modify entity @s data.tool.components."minecraft:damage" set value 249')
    s.command(AS + "function npcraft:work/commit with entity @s data.target")
    s.expect(f"if data entity {BOT} data.tool", False)
    s.expect(f"if data entity {BOT} data.cargo{{count:1}}")


def test_return_items(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:7}')
    s.command(AS + "function npcraft:commands/drop_tool")
    s.command(AS + "function npcraft:commands/drop_cargo")
    s.expect(f"if data entity {BOT} data.tool", False)
    s.expect(f"if data entity {BOT} data.cargo", False)
    s.expect('if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:iron_axe",count:1}}]')
    s.expect('if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:oak_log",count:7}}]')
    s.command(AS + "function npcraft:commands/drop_tool")
    s.command('execute store result score #items np.tmp run execute if entity @e[type=minecraft:item]')
    s.expect("if score #items np.tmp matches 2")


def test_unauthorized_and_offline(s: Server) -> None:
    s.command("scoreboard players set #actor np.tmp 2")
    s.command("scoreboard players set #cmd np.tmp 4")
    s.command("scoreboard players set #authorized np.tmp 0")
    s.command(AS + "function npcraft:commands/authorize with entity @s data")
    s.expect(f"if score {BOT} np.mode matches 0")
    s.expect("if score #authorized np.tmp matches 0")
    # Equal numeric owner still requires an authenticated actor UUID/player.
    s.command("scoreboard players set #actor np.tmp 1")
    s.command(AS + "function npcraft:commands/authorize with entity @s data")
    s.expect("if score #authorized np.tmp matches 0")
    set_target(s)
    s.command(f"scoreboard players set {BOT} np.mode 3")
    s.command(AS + "function npcraft:bot/brain with entity @s data")
    s.expect("if block 1 64 0 minecraft:oak_log")
    s.expect(f"if data entity {BOT} data.cargo", False)


def test_scheduler(s: Server) -> None:
    s.command('data modify storage npcraft:state queue set value [{id:9001},{id:999999}]')
    s.command("function npcraft:scheduler")
    s.command('execute store result score #head np.tmp run data get storage npcraft:state queue[0].id')
    s.expect('if score #head np.tmp matches 999999')
    s.command("function npcraft:scheduler")
    s.command('execute store result score #head np.tmp run data get storage npcraft:state queue[0].id')
    s.expect('if score #head np.tmp matches 9001')
    s.expect("if entity @e[tag=npcraft.nav]", False)


def test_persistence(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:23}')
    s.command('data modify storage npcraft:state queue set value [{id:9001}]')
    s.command("save-all flush")
    s.stop()
    s.start()
    s.expect(f"if data entity {BOT} data.cargo{{count:23}}")
    s.expect(f'if data entity {BOT} data{{owner_uuid:[I;0,0,0,1]}}')
    s.expect(f"if score {BOT} np.id matches 9001")
    s.expect('if data storage npcraft:state queue[{id:9001}]')
    s.expect("if score #enabled np.sys matches 0")



def test_negative_navigation(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.dest set value {x:-6,y:64,z:-1,range:0}')
    for _ in range(12):
        s.command(AS + "function npcraft:nav/plan")
    s.expect(f'if data entity {BOT} {{Pos:[-5.5d,64.0d,-0.5d]}}')
    s.expect("if entity @e[tag=npcraft.nav]", False)


def test_dismiss_conserves_items(s: Server) -> None:
    s.command(AS + 'data modify entity @s data.cargo set value {id:"minecraft:oak_log",count:11}')
    s.command('data modify storage npcraft:state queue set value [{id:9001}]')
    s.command('scoreboard players set #total np.sys 1')
    s.command(AS + "function npcraft:commands/dismiss with entity @s data")
    s.expect(f"if entity {BOT}", False)
    s.expect('if data storage npcraft:state queue[{id:9001}]', False)
    s.expect("if score #total np.sys matches 0")
    s.expect('if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:iron_axe",count:1}}]')
    s.expect('if entity @e[type=minecraft:item,nbt={Item:{id:"minecraft:oak_log",count:11}}]')
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            s.expect("if entity @e[type=minecraft:mannequin,tag=npcraft.retiring]", False)
            break
        except AssertionError:
            time.sleep(0.1)
    else:
        raise AssertionError("Retired mannequin did not disappear within five seconds")
    s.command('execute store result score #items np.tmp run execute if entity @e[type=minecraft:item]')
    s.expect("if score #items np.tmp matches 2")
    s.command("save-all flush")
    s.assert_clean_logs()


TESTS = [test_native_body, test_reload, test_wall_detour, test_far_goal, test_gap,
         test_height_and_hazard, test_scan_and_harvest, test_stale_target, test_plot_bounds,
         test_missing_tool, test_full_cargo, test_stack_and_type, test_line_of_sight,
         test_full_barrel_and_transfer, test_missing_barrel, test_axe_break,
         test_return_items, test_unauthorized_and_offline, test_scheduler, test_negative_navigation,
         test_dismiss_conserves_items, test_persistence]


from tools.agent_tests import AGENT_TESTS
TESTS.extend(AGENT_TESTS)

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--accept-eula", action="store_true", help="Accept https://aka.ms/MinecraftEULA for this isolated test server")
    parser.add_argument("--cache", type=Path, default=ROOT / ".cache/vanilla")
    parser.add_argument("--reports", type=Path, default=ROOT / "reports")
    args = parser.parse_args()
    if not args.accept_eula:
        parser.error("Explicit --accept-eula is required; no server was started")
    target = json.loads((ROOT / "project.json").read_text())
    java = subprocess.run(["java", "-version"], text=True, capture_output=True, check=True)
    match = re.search(r'version "(\d+)', java.stderr + java.stdout)
    if not match or int(match.group(1)) < target["java"]:
        parser.error(f"Java {target['java']}+ is required for Minecraft {target['minecraft']}")
    args.reports.mkdir(parents=True, exist_ok=True)
    for previous in args.reports.glob("server-*.log"):
        previous.unlink()
    suite = ET.Element("testsuite", name="vanilla-minecraft", tests=str(len(TESTS)), failures="0")
    failures = 0
    try:
        jar = download_server(target["minecraft"], args.cache.resolve())
        archive = build()
        with tempfile.TemporaryDirectory(prefix="npcraft-ci-") as directory:
            server = Server(Path(directory), jar, archive, args.reports.resolve())
            try:
                server.start()
                for test in TESTS:
                    case = ET.SubElement(suite, "testcase", name=test.__name__, classname="Vanilla26_3")
                    started = time.monotonic()
                    try:
                        fixture(server)
                        test(server)
                        server.assert_clean_logs()
                        print(f"PASS {test.__name__}", flush=True)
                    except Exception as exc:
                        failures += 1
                        ET.SubElement(case, "failure", message=str(exc)).text = traceback.format_exc()
                        print(f"FAIL {test.__name__}: {exc}", flush=True)
                    case.set("time", f"{time.monotonic() - started:.3f}")
            finally:
                server.stop()
    except Exception as exc:
        failures += 1
        case = ET.SubElement(suite, "testcase", name="server_startup")
        ET.SubElement(case, "failure", message=str(exc)).text = traceback.format_exc()
        print(f"FAIL server_startup: {exc}", file=sys.stderr)
    suite.set("tests", str(len(suite)))
    suite.set("failures", str(failures))
    ET.ElementTree(suite).write(args.reports / "vanilla.xml", encoding="utf-8", xml_declaration=True)
    print(f"Vanilla integration: {len(suite) - failures}/{len(suite)} passed")
    return int(failures != 0)


if __name__ == "__main__":
    raise SystemExit(main())
