# Architecture

```text
G / pause-menu dialog / trigger
            |
player init -> approval + Overworld + command-range checks
            |
owner ID + stored UUID validation
            |
persistent marker controller (authoritative data and scores)
            |
fair saved queue: ONE allocated record selected per server tick
            |
owner nearby? -> cooldown -> mode dispatcher
            |
follow / home / timber -> bounded navigation -> validated action
            |
mannequin presentation sync
```

## Persistent data

Each controller is a `minecraft:marker` tagged `npcraft.bot`. Marker `data` is used
because arbitrary custom fields on a mannequin are not a reliable persistence
mechanism. A `minecraft:mannequin` tagged `npcraft.body` shares its `np.id`.

Marker record:

```text
data.schema      = 1
data.id          = monotonically allocated companion ID
data.owner       = monotonically allocated player ID
data.owner_uuid  = full UUID int array copied from the player
data.home        = {x, y, z}, integer block coordinates
data.plot        = optional {x, y, z} center / ground level
data.storage     = optional {x, y, z} output barrel position
data.tool        = optional complete iron-axe item stack
data.cargo       = optional {id, count}, supported plain log only
data.target      = optional {x, y, z, kind}
data.dest        = {x, y, z, range}, navigation request
data.scan        = next index in the 196-cell plot scan
data.scanned     = cells examined since the last target, saturated at 196
```

Players keep `np.owner`, `np.sel`, `np.count` and the `npcraft` trigger. Controllers
keep `np.id`, `np.owner`, `np.mode`, `np.status`, `np.next`, `np.dig`, `np.harvest`.
Scores and marker records persist with the world. IDs are never based on “nearest
player,” never recycled on reload, and never inferred from a display name.

`npcraft:state queue` is a list of `{id}` records, including unloaded allocations.
The scheduler copies the first entry, appends it, removes the original and
processes that ID only if its controller is loaded. This prevents starvation by a
fixed selector order and prevents unloaded records from resetting allocation caps.

`npcraft:meta` stores schema, version and installation state. `np.sys` fake players
hold counters and the pause flag. Installation is gated by persistent metadata;
reload does not zero anything. Incompatible schema values fail closed.

## Temporary state and execution boundaries

Scratch storage and `#... np.tmp` scores are deliberately global. Minecraft runs
each function chain synchronously; only one controller's autonomous work chain is
entered per tick. Player requests are also processed serially. Do not add scheduled
callbacks, asynchronous work, nested work dispatch, or uncontrolled parallel
selection without first replacing the scratch-state contract.

Temporary BFS markers use `npcraft.nav`; they are removed at the end of each plan
and on load. No long-lived force-loaded pathfinding workspace is used. The direct
block/world checks operate in the current loaded dimension, supported only in the
Overworld. Scheduler macro values are server-written IDs, never arbitrary user text.

## Navigation contract

A breadth-first local search visits at most **128** cardinal cells within a
six-block radius. Nodes retain the first step from the root, not a whole path.
The first safe step is revalidated before movement. Targets farther than the local
radius may use the explored frontier with strictly lower Manhattan distance.
This is not a globally complete planner; concave obstacles can produce a safe stop.

Each candidate requires loaded chunks, a full supported floor, and clear feet/head
cells. Only a single height is supported. Navigation contains no block mutations.
The body teleports between grid cells; smooth interpolation and vertical swept
collision tests are intentionally not claimed.

## Timber transaction

Scan at most eight of the 196 plot positions per controller visit. Select only
ordinary oak/birch logs. Before cutting, validate the target still exists, bounds,
empty/matching cargo capacity, tool presence, reach and a quarter-block sampled
line of sight. Cutting takes at least 20 game ticks and can be cancelled by an order.

At commit: revalidate type/bounds/capacity/tool; remove the block without destroy
loot; only on successful removal credit the one supported log; increment tool
damage once; remove an exhausted axe; invalidate the pending target. Two workers
cannot harvest the same now-removed block successfully.

This is a synchronous logical transaction, **not a crash-proof database transaction**.
A process/power failure between world-region and scoreboard/entity saves can still
cause inconsistent snapshots. Backups and clean server shutdowns remain necessary.

A barrel transfer selects an empty slot, revalidates it, writes the supported cargo,
checks success, then removes cargo from the record. Existing stacks are not merged
or overwritten. Dismissal drops real inventory, clears the mannequin's display
copy, removes the queue entry and only then deletes the controller.

## Security boundary

The public API is a finite trigger action table. UI actions send no operator
commands and no arbitrary function names. Approved users are trusted regarding
land designation: vanilla command execution does not automatically honor external
claim plugins. Operators can directly invoke internal functions or alter NBT;
protecting a world from its own operators is outside the security model.
