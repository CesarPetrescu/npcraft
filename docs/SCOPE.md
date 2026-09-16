# Scope and acceptance criteria

## Product goal

Progress from useful companions toward independently planning survival rivals.
The current release is a tested prerequisite milestone, **not** a rival that can
fight a player or complete unrestricted survival.

## 0.2.0-alpha.1 — delivered implementation boundaries

| Stage | Delivered | Explicitly not delivered |
|---|---|---|
| Inventory | 36 persistent component-preserving slots; stack limits; staged add/take/crafting; source-preserving failure; drops and restart persistence | Native backpack GUI, armor/offhand management, backpack-to-barrel automation, unified migration of legacy cargo |
| Validated actions | Timed oak gathering; stone/cobble with supported picks; eight finite recipes; physical workbench placement; bounds, support, reach, line-of-sight, tool and capacity checks | Arbitrary blocks/loot overrides, generic recipe/loot solver, enchantment-dependent harvesting, furnaces operating automatically |
| Planning | Dependency-based empty-inventory stone kit; actual-inventory reassessment; failed-target memory and retry backoff | General GOAP, learned policy, dynamic utility system, broad world model, free-world exploration |
| Movement | Cardinal BFS with one full block up/down, support/headroom/adjacency revalidation, 128-node budget, six-block local radius | Smooth player physics, slabs/stairs, jumping gaps, two-block drops, swimming/climbing, doors/mounts/portals |
| Compatibility | Existing worker controls, approved owner ID+UUID, saved legacy tools/cargo, fair queue and pause retained | Combat, mortality, hunger, iron/diamond/Nether progression, base construction |

A stone kit is a stone pickaxe, sword, axe and furnace **item**. The agent needs a
real placed workbench for supported 3x3 recipes. It consumes every ingredient and
applies supported pickaxe wear. No item is awarded simply for entering a stage.

## Permissions and resource model

The player explicitly authorizes a **7×7×4 plot**: X/Z ±3, Y +0..+3. Autonomous
mode may gather all ordinary oak logs, stone and cobblestone in it, including
player-placed blocks. It can place its workbench in the empty plot center. It does
not recognize land ownership or distinguish building materials from resources.
Only an approved owner may issue public mutations, subject to ID+UUID and range.
The approved owner must remain within 64 blocks in the Overworld for activity.

Navigation never breaks/places blocks, changes gamerules, forces chunks or creates
rescue bridges. Unreachable resources are remembered temporarily; absence does not
mean permission to mine elsewhere. Full inventory or missing station/resources
must stop/back off without free outputs, overwritten stacks or deleted items.

The new backpack and legacy iron-axe/cargo records coexist intentionally. On upgrade,
legacy records are untouched. Unsupported module schema or incorrect bag length
fails closed. General corruption recovery and crash-consistent database semantics
are not promised; back up the complete world and shut down cleanly.

Only ordinary, breakable wooden/stone picks without explicit enchantment,
unbreakable or max-damage components are selected for autonomous mining. Other
items may be stored and returned without losing their components. Custom loot
packs, material plugins and item behaviors are not certified.

## Acceptance evidence required

Run the exact 26.3 server, not just syntax lint. Assert capacity rollback,
component-aware merging, exact recipe debits, no duplicate drops, unsupported-tool
rejection, tool breakage, station removal/reach, work boundaries/support protection,
stale targets, blocked center, missing resources, bounded memory and restart state.
Positive and negative 3D movement fixtures must cover steps, ceilings, changed
headroom, adjacency and prohibited large drops.

Run the actual graphical client with no starter-item gifts: issue one goal, observe
wooden pick and real workbench progression, obtain the final kit, then inject one
lost sword and verify replacement without another goal command. Independently
inspect returned actual inventory. Test existing worker/two-owner flows again.

A passing controlled fixture is not proof of unrestricted survival, production
performance, all Minecraft versions, accessibility, audio or public authentication.
Current results and provenance belong in AUTONOMY.md and its JSON report.
