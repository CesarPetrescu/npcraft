# Agent foundations: 0.2.0-alpha.1

## Delivered design

This milestone implements a **bounded autonomous crafting goal** on the vanilla
companion foundation. It does not implement the entire proposed survival rival.

### 1. Authoritative inventory and transactions

`data.inventory = {version:1, slots:[36 compounds]}` is stored on the controller.
An empty slot is `{}`. A filled slot is `{item:<complete item stack>, max:1|16|64}`.
The nine conceptual hotbar slots are part of the 36, not additional storage.
The legacy timber `data.tool` and `data.cargo` are deliberately left untouched.

`inventory/load` snapshots slots into command storage. Insert/remove/recipe helpers
mutate **only this snapshot**; callers commit only after every precondition and
external transfer succeeds. Failed capacity/ingredient checks discard the snapshot.
Matching is exact after normalizing count, so unlike names, enchantments and custom
data never merge. Supported max-stack sizes are read from the actual held item.

Player transfers first stage the entire stack, then clear the player hand, then
commit only on confirmed clear success. Returns summon each complete stack and
clear each slot only on success. Returns/dismissal create public drops. Invalid
operator-written records are not a supported input or an access-control boundary.

Crafting intentionally follows vanilla-like ingredient consumption: custom names
on logs/planks/sticks do not make them immune to consumption by an active goal.
Tool *storage* preserves components; tool *use* is narrower: plain wooden/stone
pickaxes with optional damage. Arbitrary enchantments are not silently simulated.

### 2. Closed action dispatch and outcomes

The public action dispatcher accepts a fixed set of server-written intents. It
never expands player-supplied function names. Results are recorded as `running`,
`blocked`, `succeeded` or `cancelled`, with a machine-readable reason. Each mining
commit revalidates allowed block type, designated plot, loaded chunk, live block,
reach/line of sight, usable pick where needed, and available backpack space.

The drop is staged before the block changes. Successful block removal precedes the
inventory commit. Pick wear is staged once, and exhaustion removes the pick. A
controller cannot mine its own support block. Navigation has no terrain permission.

The five finite recipes are oak planks, birch planks, sticks, wooden pickaxe and
stone pickaxe. Pick recipes require an assigned **real, reachable crafting table**.
Its existence is rechecked at the action boundary. Recipes consume all inputs and
reserve output capacity before committing. The agent does not place its own bench.

This is synchronous logical atomicity, not immunity to crashes between Minecraft's
separate world/entity/scoreboard persistence operations. Use consistent full backups.

### 3. Priorities and prerequisite selection

The supported goal is `stone_pickaxe`. The controller observes current inventory,
chooses a missing prerequisite, dispatches one bounded action, then observes again.
It does not maintain a fictitious technology stage separate from actual items.

```text
stone pick already present -> succeed
ready final recipe         -> craft stone pick
ready prerequisite recipe  -> craft wooden pick
usable wood pick, low stone-> mine stone
insufficient sticks        -> make sticks when planks exist
logs available             -> make planks
otherwise                  -> gather permitted logs
```

This is a finite priority/dependency planner, **not a general recipe search engine,
GOAP solver, utility learner or language model**. One concrete end-to-end goal is
used to validate the action/inventory/navigation boundaries before expanding them.
A successful goal stops harvesting and is rechecked at a reduced frequency.

World knowledge is limited to the assigned plot, workbench and current target.
After three route/visibility failures, a target is excluded temporarily. At most
eight failures are retained; memory expires after 100 game ticks. Exhausted scans
back off. It does not know unseen player positions, caves, bases or hidden ores.

The owner can cancel. Read-only dialogs/status requests preserve the current target
and cut timer. Unknown action numbers are rejected without mutating agent state.
Backpack return stops autonomous work, preventing immediate reacquisition surprises.

### 4. Conservative vertical navigation

The existing bounded BFS retains a 128-node cap and approximately six-block local
sphere. It adds walk, one-full-block ascent, and one/two-full-block descent edges.
Far-goal frontier scoring includes vertical distance. Before movement, the exact
first step is checked again against source body clearance, destination support,
destination body clearance, upward head sweep and the full drop column.

This implements **grid movement**, not continuous player physics. It does not claim
slabs/stair blocks, swimming, sprint jumps, ladders, portals, block placing/breaking,
fall-damage simulation or a globally complete 3D planner. Unsupported transitions
stop; there is no silent rescue teleport through a wall.

## Scenario and reproducibility contract

The new real-server cases cover exact-component merging, 1/16/64 stack caps, full
inventory rollback, recipe input/output accounting, missing benches, tool checks,
pick breakage, reach/plot boundaries, ascent, safe/unsafe drops, overhead/landing
changes, expiring failure memory, owner absence, additive initialization, read-only
controls, full process restart and the complete empty-backpack goal.

The new graphical scenario uses an **unmodified client** and a disclosed creative
fixture. It verifies giving/returning named stacks, assigning a real table, starting
the goal through the client, and following up three full-block steps. Starting with
an empty backpack and no mining tool, the expected resource balance is:

| Item/action | Expected after completion |
|---|---:|
| Logs removed | 2 |
| Stone removed | 3 |
| Total successful harvests | 5 |
| Stone pickaxe | 1 |
| Wooden pickaxe | 1, damage 3 |
| Unused planks | 3 |
| Sticks/cobblestone left | 0 |
| Out-of-plot log | Unchanged |

The source defines these acceptance assertions. **Only executed CI results prove
pass/fail**; adding a test does not make it pass. Graphical captures and final run
IDs are recorded in the PR/artifacts after inspection. The older gallery describes
the earlier alpha, not screenshots of these new abilities.

## Remaining milestones

A richer inventory UI/equipment controller; recipe-data-driven planning; bench
construction; iron/furnace/fuel progression; natural terrain exploration; health,
food and death recovery; combat targeting and fair last-seen opponent tracking;
building/dimensions; performance profiling. These are separate deliverables.
The current agent still pauses without an approved nearby owner. It is **not yet
an independent rival that survives, gears up and attacks you**.
