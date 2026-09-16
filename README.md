# NPCraft

[![CI](https://github.com/CesarPetrescu/npcraft/actions/workflows/ci.yml/badge.svg)](https://github.com/CesarPetrescu/npcraft/actions/workflows/ci.yml)

**Original vanilla companions that gather, craft, build workstations and can become an opt-in rival.**

**0.3.0-alpha.1 — experimental. Minecraft Java 26.3, datapack 121.0, Java 25.**
No client mod, mandatory resource pack, plugin or external AI service. Use a backed-up
world or a disposable test world. Compatibility with other game versions is not implied.

The new bounded progression chain starts with an empty backpack, not free equipment:

```text
wood -> planks/sticks -> build crafting table -> wooden pickaxe
     -> stone -> stone pickaxe + build furnace -> coal + raw iron
     -> actual furnace/fuel -> iron pickaxe -> iron sword in rival mode
```

Resources and a safe work area must exist in an assigned plot. This is **not** an
unrestricted survival player: there is no natural cave exploration, general recipe
solver, autonomous food production, armor/shield/bow manager or full player physics.

## Delivered scope

| System | Implemented behavior |
|---|---|
| Inventory | 36 full-item-record backpack slots, exact component-aware merging and staged transfers; read-only native inventory view. Legacy timber tool/cargo remain separate. |
| Planning | Finite stone-pickaxe, iron-pickaxe and rival-kit prerequisite controllers; inspect actual inventory rather than an artificial technology level. |
| Workstations | Craft and place a real crafting table and owned furnace inside the workplot, consuming materials. Mine declared supported ores and consume actual fuel in the native furnace. |
| Tools | Shared usable-tool readiness, supported wood/stone/iron picks and swords, damage and descriptive item data preserved. Unsupported mechanical components are rejected for use, not silently simulated. |
| Movement | Per-controller cached routes; cardinal full-block walk, +1 ascent, -1/-2 descent; revalidate next cell. Fast runtime work is separate from expensive round-robin planning. |
| Mortality | Explicit opt-in native health/damage, simplified supplied-food healing, single-drop inventory death handling, empty safe respawn and bounded recovery of existing marked drops. |
| Rival | Explicit consent, revocable at any distance/dimension; bounded home arena; line-of-sight last-seen memory; supported melee reach, cooldown, tool wear and low-health return-home retreat. |
| Controls | Existing companion/timber/agent menus plus iron/rival controls, backpack view, status snapshot and one-shot work-bound preview. |
| Verification | Windows/Linux quality checks, real vanilla-server suites, three actual-client GUI scenarios, multi-agent accelerated progression, artifacts and CI-gated releases. |

A configured test does not prove success: inspect the completed **Required** check,
JUnit/JSON reports, exact source SHA and reviewed screenshots. Historical galleries
remain attributed to their original versions, not relabeled as newer gameplay.

## Installation and first iron goal

Copy the **inner installable ZIP** `npcraft-0.3.0-alpha.1-mc26.3.zip` into
`<world>/datapacks/`. Remove the previous NPCraft ZIP first; never load two versions
simultaneously. GitHub's source ZIP is not itself the installable datapack.
Alternatively install the repository's `datapack/` folder so that
`<world>/datapacks/npcraft/pack.mcmeta` exists.

In game, with cheats/operator permission:

```mcfunction
/reload
/function npcraft:admin/grant
/trigger npcraft set 1
```

An operator approving someone else uses
`/execute as <actual-player-name> run function npcraft:admin/grant`.
Subsequent controls use permission-zero trigger requests, not operator powers.

Recruit a companion, select it, then set a workplot from the management panel.
The plot is **7 x 7 x 4**, X/Z +/-3 around your standing block and Y +0..+3.
**Every supported block in it is eligible, including blocks in player builds.**
Operator-approved users are trusted to designate only land they are permitted to use.
External claim plugins are not automatically honored by command-driven world edits.

Provide reachable oak/birch logs, stone, coal ore and ordinary iron ore, with clear
full-block walking lanes and adjacent space for workstations. Do not put ore under
the companion's feet: it refuses to mine its own support. The resource-finite test
layout is documented in `tools/rival_playtest.py`; arbitrary natural terrain is not
certified by that fixture. Fuel may continue burning while the NPC travels, so real
work layouts may need additional coal.

Open the new panel and start **Goal: iron pickaxe**:

```mcfunction
/trigger npcraft set 30
```

No supplied crafting table or furnace is required for the iron goal. Normal
companion work still requires its approved owner within 64 blocks in the Overworld.
A successful goal stops gathering; blocked actions report a reason rather than
creating free items. The original stone goal and timber worker remain available.

## Controls

Press G / use Quick Actions, or use `/trigger npcraft set <number>`.
Selection range is 8 blocks; ordinary orders require 16 blocks.

| Number | Action | Number | Action |
|---:|---|---:|---|
| 1 | Companion panel | 2 | Recruit |
| 3 | Select nearest owned | 4 / 5 | Follow / Stay |
| 6 / 7 | Set home / Return home | 8 / 9 | Set plot / Assign barrel beneath player |
| 10 / 11 | Timber job / Stop job | 12 / 99 | Dismiss confirmation / Confirm |
| 13 | Companion status | 14 / 15 / 16 | Give timber axe / Return axe / Return cargo |
| 20 | Stone-agent panel | 21 / 22 | Give held stack to backpack / Return backpack |
| 23 / 24 / 25 | Stone goal / Assign table below player / Agent status | 30 / 31 | Iron/rival panel / Iron goal |
| 32 / 33 / 34 | View backpack / Preview plot / Task and health snapshot | 35 | Enable mortality |
| 40 / 41 / 42 | Rival consent screen / Accept / End rival globally | | |

Returning items or dismissing creates **public item drops**. Others can pick them
up. Backpack return stops work first. Views and unknown requests do not reset
pending work. 36 slots include the conceptual nine hotbar slots, not 36 plus nine.
The inventory view is **read-only**, not a drag-and-drop chest interface.

The timber worker still uses its given ordinary unenchanted iron axe and separate
single-type log cargo, depositing only into assigned barrel empty slots. New
backpack tools do not silently replace this legacy system.

## Mortality and a first rival match

Supply food through **Give held stack** before enabling mortality. This version
uses cooked beef, bread or apples; it does not hunt/farm for them. Mortality remains
enabled after leaving rival mode. Native health/damage is authoritative, but the
food meter and healing are deliberately simplified, not full vanilla player hunger.

For a duel, stand in Survival or Adventure near your selected owned companion,
configure its plot/home, open **Start rival...**, read the warning and accept.
It builds a supported kit from permitted resources and attacks only **you**, the
consenting player. It never chooses arbitrary other users as opponents.

The arena is home X/Z +/-16, Y +/-8. It can sense the opponent within 16 blocks only
with line of sight; hidden positions do not refresh last-seen memory. Melee uses
2.8-block reach, a 20-tick cooldown and real tool wear. Low native health triggers
a simple return-home retreat, not sophisticated combat tactics.

Exit from anywhere, including another dimension or after approval is revoked:

```mcfunction
/trigger npcraft set 42
```

Consent epochs and persistent ACL checks prevent an old unloaded rival from becoming
active under a later unrelated opt-in. Rival thinking may continue without owner
proximity **only while its chunk is loaded** and consent/approval remain valid.
No offline resources are invented, and the datapack never force-loads chunks.

On death, authoritative carried items drop once. After a delay it can respawn empty
at a safe loaded home and attempt to recover actual nearby marked loot. Stolen,
burned, despawned or unreachable items are not recreated. Workstations remain in
the world with any inputs/fuel/output still in them; death is not a rollback.

## Server operations

```mcfunction
/function npcraft:admin/pause
/function npcraft:admin/resume
/execute as <player> run function npcraft:admin/revoke
```

Approval and ordinary ownership are separate from rival consent. Pause stops work
and combat but does not make mortal bodies immune to external damage. Save backups
of the **whole world**, including entity regions, scoreboards and command storage.
Synchronous item staging is not crash-proof atomicity across separate save files.

Load and dismiss all companions, collect their returned items, and account for
station contents before uninstalling. Removing the ZIP alone leaves saved entities.
Do not blindly `/kill` controllers or reset allocation counters: unloaded does not
mean deleted. See [operations](docs/OPERATIONS.md).

## Develop, test, release

Python 3.13, Java 25. Core tools use Python's standard library.

```sh
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build.py
python tools/server_test.py --accept-eula
python tools/v03_adversarial_tests.py --accept-eula --reports reports/adversarial
python tools/reliability_tests.py --accept-eula --reports reports/reliability
python tools/soak_test.py --accept-eula --agents 1,4,8,16 --ticks 6000
```

Review the Minecraft EULA before passing `--accept-eula`. Runtime tests use disposable
loopback-only worlds. GUI tests additionally use Xvfb/Mesa, xdotool and ImageMagick;
see `.github/workflows/client-playtest.yml` for exact setup and the three commands.
No game binaries, account tokens, server properties or world saves are committed.

The multi-agent run uses accelerated **tick sprint** and declared resource plots.
It checks sustained production logic and item accounting, not natural-world success,
human latency, GPU performance or production capacity on your server.

**Required** aggregates quality, vanilla, graphical and multi-agent jobs. The tag
publisher reuses that full workflow. Branch protection must separately require the
check; this repository code does not alter merge policies or create a release.

[Current contract](docs/IRON_SURVIVAL_RIVAL.md) · [Scope](docs/SCOPE.md) ·
[Architecture](docs/ARCHITECTURE.md) · [Testing](docs/TESTING.md) ·
[Roadmap](docs/ROADMAP.md) · [Contributing](CONTRIBUTING.md)

## License

Original MIT-licensed implementation. No paid Marketplace code/assets or third-party
pathfinder copied. Not an official Minecraft product; not approved by or associated
with Mojang or Microsoft.
