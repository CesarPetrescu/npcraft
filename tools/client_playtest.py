#!/usr/bin/env python3
"""Exercise the real vanilla GUI on an isolated loopback test server, capture PNGs.

Requires Java 25, Xvfb, Mesa, xdotool and ImageMagick. GUI input is sent to the
unmodified client. RCON constructs the fixture and independently verifies state;
it does not impersonate the player's trigger requests. No account/token is used.
"""
from __future__ import annotations
import argparse
from contextlib import suppress
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.build import ROOT, build
from tools.server_test import Server, download_server
from tools.client_install import install

PLAYER = 'NPCraftQA'
BOT = '@e[type=minecraft:marker,tag=npcraft.bot,limit=1]'


class Client:
    def __init__(self, root: Path, game: Path, reports: Path, port: int):
        self.root, self.game, self.reports = root, game, reports
        self.port = port
        self.process = None
        self.window = None
        self.log = None

    def start(self, meta, classpath, natives):
        self.game.mkdir(parents=True, exist_ok=True)
        settings = {'renderDistance': 4, 'simulationDistance': 4, 'maxFps': 30,
                    'enableVsync': 'false', 'fullscreen': 'false', 'guiScale': 2,
                    'graphicsMode': 0, 'ao': 'false', 'cloudStatus': 'false',
                    'tutorialStep': 'none', 'onboardAccessibility': 'false',
                    'skipMultiplayerWarning': 'true', 'narrator': 0,
                    'soundCategory_master': 0.0, 'pauseOnLostFocus': 'false',
                    'bobView': 'false', 'fov': 0.0}
        (self.game / 'options.txt').write_text(''.join(f'{k}:{v}\n' for k,v in settings.items()))
        ident = bytearray(hashlib.md5(('OfflinePlayer:' + PLAYER).encode()).digest())
        ident[6] = (ident[6] & 15) | 48
        ident[8] = (ident[8] & 63) | 128
        args = ['java', '-Xms512M', '-Xmx2048M', '-XX:ActiveProcessorCount=2',
                '-Djava.library.path=' + str(natives), '-Dorg.lwjgl.system.SharedLibraryExtractPath=' + str(natives),
                '-cp', os.pathsep.join(map(str, classpath)), meta['mainClass'],
                '--username', PLAYER, '--uuid', uuid.UUID(bytes=bytes(ident)).hex,
                '--accessToken', '0', '--userType', 'msa', '--version', meta['id'],
                '--versionType', 'release', '--gameDir', str(self.game),
                '--assetsDir', str(self.root / 'assets'), '--assetIndex', meta['assetIndex']['id'],
                '--width', '1280', '--height', '720',
                '--quickPlayMultiplayer', '127.0.0.1:' + str(self.port),
                '--quickPlayPath', str(self.game / 'quickplay.json')]
        self.log = (self.reports / 'client-console.log').open('w')
        self.process = subprocess.Popen(args, cwd=self.game, stdout=self.log, stderr=subprocess.STDOUT)

    def key(self, key: str):
        subprocess.run(['xdotool', 'key', '--clearmodifiers', key], check=True)
        time.sleep(0.25)

    def chat(self, command: str):
        self.key('t')
        subprocess.run(['xdotool', 'type', '--clearmodifiers', '--delay', '15', '--', command], check=True)
        self.key('Return')
        time.sleep(0.75)

    def shot(self, name: str):
        # Capture the actual X framebuffer. No generated rendering or image overlays.
        time.sleep(1.5)
        destination = self.reports / 'screenshots' / (name + '.png')
        destination.parent.mkdir(exist_ok=True)
        subprocess.run(['import', '-window', 'root', str(destination)], check=True)
        return destination

    def focus(self):
        output = subprocess.run(['xdotool', 'search', '--onlyvisible', '--name', 'Minecraft'], text=True, capture_output=True)
        if output.returncode == 0 and output.stdout.strip():
            self.window = output.stdout.strip().splitlines()[-1]
            subprocess.run(['xdotool', 'windowfocus', '--sync', self.window], check=True)
            return True
        return False

    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
        if self.log:
            self.log.close()
        if (self.game / 'logs/latest.log').exists():
            shutil.copy2(self.game / 'logs/latest.log', self.reports / 'client-latest.log')


def run(args):
    reports = args.reports.resolve()
    reports.mkdir(parents=True, exist_ok=True)
    result = {'minecraft': '26.3', 'source_commit': os.environ.get('GITHUB_SHA', 'local'),
              'run_id': os.environ.get('GITHUB_RUN_ID'), 'method': 'unmodified vanilla GUI + xdotool; loopback RCON assertions',
              'checks': [], 'screenshots': [], 'success': False}
    def check(name, fn):
        fn()
        result['checks'].append({'name': name, 'passed': True})
        print('PASS ' + name, flush=True)
    meta, cp, natives = install('26.3', args.cache.resolve() / 'client')
    jar = download_server('26.3', args.cache.resolve() / 'server')
    with tempfile.TemporaryDirectory(prefix='npcraft-visual-') as tmp:
        root = Path(tmp)
        server = Server(root / 'server', jar, build(), reports)
        # Expose the independently chosen game port to the client, disable profile requirement only locally.
        props = server.work / 'server.properties'
        settings = dict(line.split('=', 1) for line in props.read_text().splitlines())
        settings.update({'max-players': '2', 'enforce-secure-profile': 'false',
                         'gamemode': 'creative', 'difficulty': 'peaceful', 'view-distance': '4'})
        props.write_text(''.join(f'{k}={v}\n' for k,v in settings.items()))
        client = Client(args.cache.resolve() / 'client', root / 'client', reports, int(settings['server-port']))
        try:
            server.start()
            c = server.command
            c('forceload add -32 -32 32 32')
            time.sleep(3)
            c('fill -20 63 -20 24 63 20 minecraft:grass_block')
            c('fill -20 64 -20 24 70 20 minecraft:air')
            c('setworldspawn 0 64 6')
            c('time set noon')
            c('weather clear')
            # World edits are fixture construction, never datapack navigation actions.
            for command in ['gamerule minecraft:advance_time false', 'gamerule minecraft:advance_weather false']:
                with suppress(AssertionError):
                    c(command)
            # A bounded demonstration grove; the actual harvest is not precomputed.
            for x,z in [(-2,-2),(2,-2),(-2,2),(2,2)]:
                c(f'fill {x} 64 {z} {x} 67 {z} minecraft:oak_log')
                c(f'fill {x-1} 68 {z-1} {x+1} 68 {z+1} minecraft:oak_leaves[persistent=true]')
            c('setblock 0 63 4 minecraft:barrel[facing=up]')
            c('fill -4 63 -4 4 63 -4 minecraft:birch_planks')
            c('fill -4 63 3 4 63 3 minecraft:birch_planks')
            c('fill -4 63 -3 -4 63 2 minecraft:birch_planks')
            c('fill 4 63 -3 4 63 2 minecraft:birch_planks')
            c('fill 8 64 -2 8 65 2 minecraft:stone_bricks')
            # Protected display building is outside the 7x7 plot.
            c('fill -12 64 -9 -8 66 -5 minecraft:oak_planks hollow')
            c('fill -13 67 -10 -7 67 -4 minecraft:spruce_planks')
            client.start(meta, cp, natives)
            deadline = time.monotonic() + 150
            while time.monotonic() < deadline:
                if client.process.poll() is not None:
                    raise RuntimeError('Minecraft client exited; inspect client-console.log')
                client.focus()
                if PLAYER in c('list'):
                    break
                time.sleep(2)
            else:
                raise TimeoutError('Graphical client did not join local server')
            time.sleep(8)
            client.focus()
            check('real_client_joined', lambda: server.expect('if entity @a[name=' + PLAYER + ']'))
            c(f'execute as {PLAYER} run function npcraft:admin/grant')
            c(f'tp {PLAYER} 0.5 64 0.5 180 10')
            client.chat('/trigger npcraft set 2')
            check('non_operator_recruit', lambda: server.expect('if entity ' + BOT))
            c(f'tp {PLAYER} 5.5 64 7.5 145 10')
            result['screenshots'].append(client.shot('01-companion-in-world').name)
            client.key('g')
            result['screenshots'].append(client.shot('02-native-management-panel').name)
            client.key('Escape')
            # Axe transfer travels through the client's permission-zero command.
            c(f'item replace entity {PLAYER} weapon.mainhand with minecraft:iron_axe')
            client.chat('/trigger npcraft set 14')
            check('real_player_axe_transfer', lambda: server.expect(f'if data entity {BOT} data.tool'))
            check('axe_removed_from_player', lambda: server.expect(f'if items entity {PLAYER} weapon.mainhand minecraft:iron_axe', False))
            # Set plot and barrel using player-location semantics.
            c(f'tp {PLAYER} 0.5 64 0.5 180 0')
            client.chat('/trigger npcraft set 8')
            check('plot_assigned', lambda: server.expect(f'if data entity {BOT} data.plot{{x:0,y:64,z:0}}'))
            c(f'tp {PLAYER} 0.5 64 4.5 180 0')
            client.chat('/trigger npcraft set 9')
            check('barrel_assigned', lambda: server.expect(f'if data entity {BOT} data.storage{{x:0,y:63,z:4}}'))
            c(f'tp {PLAYER} 5.5 64 7.5 145 10')
            client.chat('/trigger npcraft set 10')
            check('job_started_through_client', lambda: server.expect(f'if score {BOT} np.mode matches 3'))
            time.sleep(4)
            result['screenshots'].append(client.shot('03-timber-worker').name)
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                response = c('data get block 0 63 4 Items')
                if 'oak_log' in response:
                    break
                time.sleep(2)
            else:
                raise AssertionError('Autonomous worker did not deposit logs within 90 seconds: ' + c(f'data get entity {BOT} data'))
            check('autonomous_harvest_and_deposit', lambda: server.expect('if data block 0 63 4 Items[{id:"minecraft:oak_log"}]'))
            check('building_outside_plot_untouched', lambda: server.expect('if block -12 64 -9 minecraft:oak_planks'))
            client.chat('/trigger npcraft set 11')
            c(f'tp {PLAYER} 0.5 64 5.5 180 65')
            result['screenshots'].append(client.shot('04-harvested-plot').name)
            # Actual right-click opens the assigned barrel GUI.
            c(f'tp {PLAYER} 0.5 64 4.5 0 90')
            time.sleep(1)
            subprocess.run(['xdotool','click','3'], check=True)
            result['screenshots'].append(client.shot('05-barrel-inventory').name)
            client.key('Escape')
            c(f'tp {PLAYER} 6.5 64 0.5 -90 0')
            client.chat('/trigger npcraft set 4')
            c(f'tp {PLAYER} 12.5 64 0.5 90 5')
            time.sleep(8)
            check('follow_around_wall', lambda: server.expect(f'if entity @e[type=minecraft:marker,tag=npcraft.bot,x=12.5,y=64,z=0.5,distance=..2.5]'))
            check('navigation_preserved_wall', lambda: server.expect('if block 8 64 0 minecraft:stone_bricks'))
            result['screenshots'].append(client.shot('06-follow-obstacle-course').name)
            client.chat('/trigger npcraft set 5')
            check('stay_through_client', lambda: server.expect(f'if score {BOT} np.mode matches 0'))
            # Vanilla save/reload with an actual player and owner UUID.
            c('reload')
            time.sleep(3)
            check('owner_and_companion_survive_reload', lambda: server.expect(f'if entity {BOT}'))
            server.assert_clean_logs()
            result['success'] = True
        except Exception as exc:
            result['failure'] = str(exc)
            result['traceback'] = traceback.format_exc()
            print(traceback.format_exc(), flush=True)
            with suppress(Exception):
                client.shot('failure')
            with suppress(Exception):
                result['bot_state'] = server.command(f'data get entity {BOT} data')
                result['bot_scores'] = server.command(f'scoreboard players list {BOT}')
        finally:
            client.stop()
            server.stop()
            result['screenshots'] = sorted(p.name for p in (reports / 'screenshots').glob('*.png')) if (reports / 'screenshots').exists() else []
            (reports / 'visual-results.json').write_text(json.dumps(result, indent=2) + '\n')
    return 0 if result['success'] else 1


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accept-eula', action='store_true')
    p.add_argument('--cache', type=Path, default=ROOT / '.cache/visual')
    p.add_argument('--reports', type=Path, default=ROOT / 'reports/visual')
    args = p.parse_args()
    if not args.accept_eula:
        p.error('Explicit --accept-eula is required for the isolated server')
    raise SystemExit(run(args))
