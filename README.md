# NPCraft

[![CI](https://github.com/CesarPetrescu/npcraft/actions/workflows/ci.yml/badge.svg)](https://github.com/CesarPetrescu/npcraft/actions/workflows/ci.yml)

**Vanilla Minecraft companions with bounded, resource-accounted autonomy.**

NPCraft **0.2.0-alpha.1** adds an autonomous stone-kit agent to the existing timber
companions. Assign an authorized plot and one goal; the agent gathers resources,
crafts and places a real workbench, makes its first pickaxe, mines stone, and
produces a stone pickaxe, sword, axe and furnace. Missing equipment causes replanning.
No client mod, resource pack, external AI service, or Python process is needed in-game.

> **Experimental alpha, not a full survival opponent.** Bodies remain invulnerable.
> Navigation is grid-stepped with conservative one-full-block up/down transitions.
> There is no PvP, hunger, mortality, smelting, iron progression, unrestricted
> exploration, or portal travel. Use a new test world or a complete world backup.

## Implemented versus planned

| System | Implemented in this alpha |
|---|---|
| Companion management | Recruit, select, follow, stay, home, status, dismiss; native dialogs and trigger controls |
| Inventory | Persistent **36-slot backpack**, component-aware stacking, native item stack limits, capacity checks and staged transactions |
| Autonomous decisions | Finite dependency planner for a **stone kit**, re-evaluating actual inventory, bounded resource scans and expiring failed-target memory |
| Actions | Whitelisted timed gathering, tool checks/wear, ingredient-consuming recipes, real workbench placement and reach validation |
| Navigation | Bounded local BFS; cardinal movement and one-full-block up/down steps; clearance/support rechecks; no digging or bridging to navigate |
| Ownership | Operator approval, owner ID plus UUID, local command range, approved nearby owner required for activity |
| Legacy timber worker | Assigned oak/birch plot, transferred iron axe, single-type cargo and empty-slot barrel deposits remain available |
| Evidence | Actual vanilla server tests and graphical client acceptance, screenshots and machine-readable results |

The new backpack is separate from the **legacy iron axe and cargo**. No automatic
conversion, general armor/offhand manager, drag-and-drop backpack GUI, or automatic
backpack-to-barrel unloading is implemented. The legacy barrel routine still manages
legacy cargo only. See [scope](docs/SCOPE.md) and [autonomy details](docs/AUTONOMY.md).

## Compatibility

| Component | Target |
|---|---|
| Game | **Minecraft Java 26.3**, vanilla server / singleplayer |
| Datapack format | **121.0**, exact target |
| Server runtime | **Java 25+** |
| Development tools | Python **3.13**, standard library only |
| Optional graphical tests | Linux, Java 25, Xvfb, Mesa, xdotool, ImageMagick |

Do not silence older/newer-version warnings by editing the pack format. Bedrock,
Paper/Fabric behavior, Realms deployment and future versions are not certified.
Primary version references are in [SOURCES.md](docs/SOURCES.md).

## Install or upgrade

Download the **inner installable ZIP** from a successful CI run's `npcraft-datapack`
artifact, or a published release, and put it in:

```text
<world>/datapacks/npcraft-0.2.0-alpha.1-mc26.3.zip
```

Do not install GitHub's source-code ZIP. From a source checkout, copying the
`datapack/` directory into `<world>/datapacks/npcraft/` also works; `pack.mcmeta`
must be directly inside it. Generated runtime functions are included in the repo.

For an upgrade, back up the entire world, **replace** the old ZIP/folder rather
than install two copies, and `/reload`. Existing IDs, owners, legacy cargo, pause
state and tools remain unchanged. The new module is initialized lazily when used.

An operator approves each user:

```mcfunction
/reload
/execute as <player> run function npcraft:admin/grant
```

Replace `<player>` with the actual name. From your own in-game chat,
`/function npcraft:admin/grant` approves yourself. All normal controls afterwards
are permission-zero triggers, not operator commands.

## First autonomous agent

1. In the Overworld, stand on clear full-block ground. Use the **G** legacy menu
   to recruit a companion, or `/trigger npcraft set 2`. It becomes selected.
2. Stand at your intended plot center and `/trigger npcraft set 8`. The plot is
   X/Z **±3**, Y **+0 through +3**, relative to your feet.
3. Move off the center and keep its block empty: the agent needs it for its
   workbench. Supply reachable ordinary **oak logs** and exposed **stone or
   cobblestone** inside the plot. The demonstration requires three logs and sixteen
   stone, but extra resources help with obstructions, tool replacement and retries.
4. Open `/trigger npcraft set 20` and choose **Build stone kit**, or send
   `/trigger npcraft set 21`. Do **not** give it starter tools for the empty-inventory
   demonstration. It chooses the prerequisite gathering/crafting tasks itself.
5. Stay nearby. Read **Task / inventory status** to see progress or why it stopped.
   A blocked center must be cleared by you; a full bag must be emptied. The agent
   does not break an obstruction simply because it wants the space.

**All eligible oak, stone and cobblestone inside this plot are permitted—including
player builds.** Work boundaries are not automatic land-claim integration. Only
approve users trusted to designate allowed land. Place protected builds outside.

```text
One goal: stone kit
  -> gather oak by hand -> planks / sticks / workbench
  -> place workbench -> wooden pickaxe
  -> mine stone -> stone pickaxe / sword / axe / furnace
  -> wait and reassess actual inventory; replace missing supported equipment
```

The furnace is a **crafted item**, not an autonomous smelting system. A crafted
sword is not combat AI. The planner follows a small reviewed recipe dependency
network, not an LLM, learned policy, arbitrary recipe solver, or dynamic utility AI.

### Autonomous controls

| Trigger | Action |
|---:|---|
| 20 | Open the autonomous-agent panel |
| 21 | Start / resume the stone-kit goal |
| 22 | Transfer the actual held item stack into the backpack |
| 23 | Return backpack as physical item drops |
| 24 | Show task and backpack state in chat |
| 25 | Stop autonomy and cancel pending harvest |

Use `/trigger npcraft set <number>`. **Stop before returning the backpack** unless
you intend it to replenish the missing kit. Anyone can pick up world drops nearby.
Normal tool components and native stack limits are preserved by backpack transfer;
only standard breakable, unenchanted wooden/stone picks are supported for mining.
Conservatively, explicit enchantment/max-damage/unbreakable overrides are not used.

### Existing companion / timber controls

| Trigger | Action | Trigger | Action |
|---:|---|---:|---|
| 1 | Legacy panel | 2 | Recruit |
| 3 | Select nearest owned | 4 | Follow |
| 5 | Stay | 6 | Set home at your feet |
| 7 | Return home | 8 | Assign work plot |
| 9 | Assign barrel beneath you | 10 | Start legacy timber job |
| 11 | Stop legacy job | 12 | Dismissal confirmation |
| 13 | Legacy status | 14 | Give held unenchanted iron axe |
| 15 | Return legacy axe | 16 | Return legacy cargo |
| 99 | Confirm dismissal | | |

The timber job still harvests oak/birch with its **legacy** iron axe and deposits
legacy cargo into an assigned barrel's **empty** slots. Stand on the barrel when
assigning it; provide a supported reachable approach. Existing stacks are not merged
by that older transfer routine. For the legacy walkthrough and captured evidence,
see [the original client playtest](docs/CLIENT_PLAYTEST.md).

Selection: **8 blocks**. Orders: **16 blocks**. Activity requires the approved owner
within **64 blocks**, in the same Overworld. Allocation caps remain **4 per owner /
16 globally**, including unloaded companions. These are safety limits, not measured
production capacity. No production chunks are force-loaded.

## Tests, screenshots and development

See the [autonomous agent report and gallery](docs/AUTONOMY.md),
[testing contract](docs/TESTING.md), and [architecture](docs/ARCHITECTURE.md).
The earlier worker's [seven-image gallery](docs/CLIENT_PLAYTEST.md) remains a
historical record, not evidence of every new feature.

```sh
python tools/generate_agent.py --check
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build.py
```

Edit `tools/generate_agent.py` for generated agent resources, then run it without
`--check` and commit **both generator and generated files**. Old companion/navigation
resources are still directly maintained. No `pip install` is needed for these checks.

Review the [Minecraft EULA](https://aka.ms/MinecraftEULA) before running server tests:

```sh
python tools/server_test.py --accept-eula --reports reports/legacy
python tools/agent_test.py --accept-eula --reports reports/agent
```

Both boot official, exact-version vanilla in isolated disposable loopback worlds.
They do not open your saves. Graphical CI also runs the actual unmodified client:
keyboard/mouse sends player requests, RCON prepares fixtures and checks outcomes.
This is automated testing, not an unrestricted human survival playthrough.

The `Required` gate combines Linux/Windows offline quality, both vanilla suites,
and both graphical suites. No failed/skipped dependency counts as success. Configure
that check separately in GitHub branch protection. Tag releases run the same gate
before publishing; no release is automatically created by a PR.

## Administration and removal

```mcfunction
/function npcraft:admin/pause
/function npcraft:admin/resume
/execute as <player> run function npcraft:admin/revoke
```

Revocation/pause preserves items and allocations. Do not run blanket `/kill` on
controllers: the marker owns the real inventory, and the mannequin is a cosmetic
copy. Load each companion's area, stop it, return inventory or dismiss normally,
and collect drops before removing the pack. Deleting the ZIP alone leaves saved
entities/state. See [operations](docs/OPERATIONS.md).

## License

Original implementation: MIT. No paid Marketplace code/assets, third-party
pathfinder, Minecraft binaries, private credentials or saved test worlds are
redistributed. Not an official Minecraft product; not approved by or associated
with Mojang or Microsoft.
