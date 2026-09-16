# NPCraft

[![CI](https://github.com/CesarPetrescu/npcraft/actions/workflows/ci.yml/badge.svg)](https://github.com/CesarPetrescu/npcraft/actions/workflows/ci.yml)
[![Graphical playtest](https://github.com/CesarPetrescu/npcraft/actions/workflows/client-playtest.yml/badge.svg)](https://github.com/CesarPetrescu/npcraft/actions/workflows/client-playtest.yml)

**Controllable vanilla Minecraft companions with resource-accounted autonomous goals.**

> **0.2.0-alpha.1 — experimental. Use a backup or a disposable world.**
> This is a worker/agent foundation, not a complete survival player or PvP opponent.
> Bodies are invulnerable; movement is grid-stepped. No client mod, mandatory
> resource pack, language model or external AI service is needed.

## Compatibility

| Component | Target |
|---|---|
| Game | Minecraft **Java 26.3**, vanilla |
| Datapack | **121.0**, exact tested target |
| Server runtime | Java **25+** |
| Build/tests | Python **3.13**, standard library |
| Optional graphical tests | Linux, Xvfb/Mesa, xdotool, ImageMagick |

See [primary version references](docs/SOURCES.md). Editing pack.mcmeta is not proof
of compatibility with another game version. Bedrock, Paper/Fabric-specific behavior
and Realms are not certified.

## What is here

| System | Implemented behavior |
|---|---|
| Companion | Mannequin presentation, persistent marker controller, stable owner/companion IDs |
| Controls | Recruit/select, follow/stay/home, jobs, diagnostics, inventory return and dismissal |
| Authorization | Explicit operator approval, owner ID **plus UUID**, range checks |
| Navigation | Bounded cardinal BFS; full-block walk, ascend one block, descend at most two; source/landing and overhead checks |
| Timber job | Timed oak/birch harvesting inside a designated 7 x 7 x 4 plot; real iron axe and barrel deposits |
| Agent backpack | 36 slots, complete item-stack records, exact-component merging, supported stack limits 1/16/64 |
| Action API | Closed mine/craft actions; revalidated reach, permissions, resources and capacity; explicit outcome/reason |
| Goal planner | An empty backpack to a stone pickaxe, choosing resource and recipe prerequisites automatically |
| Memory/recovery | Bounded, expiring failed-target memory; backoff and owner cancellation |
| Distribution | Deterministic installable ZIP and SHA-256; unit, vanilla-server and graphical CI |

The planner is a finite dependency controller, **not general GOAP or an LLM**. The
backpack's 36 slots already include the conceptual nine hotbar slots; it is not
36 + 9. There is no drag-and-drop backpack screen, armor/offhand manager or hunger
system yet. The old timber axe/cargo remain separate to preserve existing saves.

## Install

Use a successful CI run's `npcraft-datapack` artifact or a published release. The
artifact may be an outer ZIP; install the **inner** file:

```text
<world>/datapacks/npcraft-0.2.0-alpha.1-mc26.3.zip
```

Do not install GitHub's source ZIP. Alternatively copy the repository's `datapack/`
directory so `<world>/datapacks/npcraft/pack.mcmeta` exists. In-game, as an operator:

```mcfunction
/reload
/function npcraft:admin/grant
/trigger npcraft set 1
```

The grant command approves the executing player. From a server console, approve
someone explicitly with `execute as <player> run function npcraft:admin/grant`.
Normal controls then use permission-zero `/trigger` requests.

## Autonomous stone-pickaxe demonstration

1. Recruit a companion on supported full-block ground in the Overworld. Do not
   give it a tool or resources: it can harvest the supported logs by hand.
2. Stand at the center of an allowed work plot and use `/trigger npcraft set 8`.
   The plot is X/Z +/-3 from that block and Y +0..+3. **Every supported block in the
   plot is eligible**, including player-placed building blocks. Exclude buildings.
3. Supply a reachable **real crafting table**. Stand on it and issue
   `/trigger npcraft set 24`. A table embedded flush with the ground makes the
   first demonstration simple. The agent does not create its own table yet.
4. Ensure the plot contains at least **two ordinary oak/birch logs and three
   exposed stone/cobblestone blocks**, with clear approaches. An accessible test
   plot is not a substitute for unlimited cave/exploration capability.
5. Use `/trigger npcraft set 20` for the agent panel, then **Make stone pickaxe**,
   or use `/trigger npcraft set 23`. Remain within 64 blocks.

The controller chooses prerequisites, rather than requiring commands per step:

```text
Gather logs -> craft planks/sticks -> craft wooden pickaxe
            -> mine three stone blocks -> craft stone pickaxe -> finish
```

Inputs are consumed; there is no free gear. Starting empty, the supported recipe
chain uses two logs, produces eight planks, turns two planks into four sticks,
uses three planks/two sticks for the wooden pick, mines three cobblestone, and
consumes the cobblestone/two sticks for the stone pick. Three planks remain, and
the wooden pick has three durability uses. Output stays in the backpack.

`/trigger npcraft set 25` shows the goal state, reason and backpack records.
`/trigger npcraft set 11` cancels work. Opening/status controls do not restart a cut.
To return the backpack, use `/trigger npcraft set 22`: work stops and contents are
**public item drops at the companion**, not private delivery to your inventory.

## Controls

Select the nearest owned companion within **8 blocks**. Orders require the selected
companion within **16 blocks**. Autonomous work requires the approved owner within
**64 blocks** in the Overworld. Offline/unloaded/out-of-range workers pause; no chunks
are force-loaded. Allocation caps are 4 per owner / 16 globally, not measured capacity.

| Trigger value | Action | Trigger value | Action |
|---:|---|---:|---|
| 1 | Original G/pause panel | 2 | Recruit |
| 3 | Select nearest owned | 4 | Follow |
| 5 | Stay | 6 | Set home here |
| 7 | Return home | 8 | Set work plot here |
| 9 | Assign barrel beneath player | 10 | Start original timber job |
| 11 | Stop/cancel | 12 | Dismiss confirmation |
| 13 | Original status | 14 | Give held iron axe to timber job |
| 15 | Return timber axe | 16 | Return timber cargo |
| 20 | Agent/backpack panel | 21 | Give held stack to backpack |
| 22 | Stop and return backpack | 23 | Make stone pickaxe goal |
| 24 | Assign crafting table beneath player | 25 | Agent/backpack status |
| 99 | Confirm dismissal | | |

Use `/trigger npcraft set <value>`. The existing G/pause menu is preserved; the new
agent panel is opened using value 20. Inventory transfers support full item data,
but **using** every stored item/enchantment in AI is not implemented. Mining picks
are restricted to plain wooden/stone picks, with optional durability damage.

## Original timber worker

Assign a plot (8), stand on an output barrel and assign it (9), give a normal
unenchanted iron axe (14), then start the timber job (10). The legacy load is one
stack of oak/birch logs; deposits use empty barrel slots, not stack merging. Full or
missing barrels preserve cargo. This mode does not use the new backpack for output.

## Safety and limitations

Navigation never breaks or places blocks. It checks full-block support and two
clear body cells, plus the swept overhead/drop column. One-block ascents and drops
up to two blocks are supported; slabs, stair-shaped blocks, swimming, ladders,
doors, portals, bridging and general parkour are not. Movement remains discrete,
not a physical jump animation. Bounded search may safely stop at complex obstacles.

Only operator-approved users may control companions. Approved users are trusted to
designate permitted land: vanilla commands do not automatically honor claim plugins.
The goal's allowed harvest set is oak/birch logs, stone and cobblestone in the plot.
No ores, arbitrary block loot/enchantment semantics or custom recipe discovery.

No health/hunger/death progression, combat/PvP, base building, unrestricted world
memory or independent offline rivals are implemented. See [scope](docs/SCOPE.md)
and [the next milestones](docs/ROADMAP.md), not marketing claims, for the boundary.

Back up the **whole world**. Inventory transactions are synchronous logical changes,
not crash-proof cross-region database commits. Agent state is added lazily without
resetting existing UUIDs, timber items or counters. Do not downgrade after storing
backpack items. Dismiss loaded companions and collect all drops before uninstalling.
Do not use blanket `/kill`: the invisible marker owns the authoritative inventory.

```mcfunction
/function npcraft:admin/pause
/function npcraft:admin/resume
/execute as <player> run function npcraft:admin/revoke
```

## Build, tests and evidence

```sh
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build.py
python tools/server_test.py --accept-eula
```

The server test requires Java 25 and explicit [Minecraft EULA](https://aka.ms/MinecraftEULA)
acceptance. It downloads the exact official server with size/hash checks and runs
only a disposable loopback world. Graphical CI additionally runs:

```sh
xvfb-run -a python tools/client_playtest.py --accept-eula
xvfb-run -a python tools/agent_playtest.py --accept-eula
```

These use real unmodified game clients with synthetic local identities. RCON sets
up disclosed fixtures and checks state; player requests originate from GUI input.
Logs/results/captures are artifacts. A successful automated scenario is not a claim
of a human survival playthrough or production performance.

[Agent design and test contract](docs/AGENT_FOUNDATIONS.md) ·
[Earlier two-client gallery](docs/CLIENT_PLAYTEST.md) ·
[Architecture](docs/ARCHITECTURE.md) · [Operations](docs/OPERATIONS.md) ·
[Testing](docs/TESTING.md) · [Contribution guide](CONTRIBUTING.md)

## License

Original code is MIT. No paid Marketplace code/assets or third-party pathfinder is
copied. No Minecraft binaries, textures, accounts or credentials are redistributed.
Not an official Minecraft product; not approved by or associated with Mojang/Microsoft.
