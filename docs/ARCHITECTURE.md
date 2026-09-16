# Architecture

```text
Actual player trigger / native dialog
           |
approval + dimension + range + owner ID and UUID
           |
persistent marker controller
           |
fair queue: one allocated record selected per server tick
           |
approved owner nearby? -> cooldown -> selected mode
           |
follow / home / legacy timber / agent goal
           |
bounded navigation + validated world/inventory actions
           |
mannequin presentation sync
```

## Authoritative state

`minecraft:marker` with tag `npcraft.bot` holds custom `data` and controller scores.
A `minecraft:mannequin` with tag `npcraft.body` shares its `np.id`. The mannequin is
an invulnerable cosmetic body, not an authenticated player and not an item store.

Core marker record: schema, stable companion ID, numeric owner ID, full owner UUID,
home/work-plot/output-container coordinates, navigation destination, target and scan
cursor. Legacy timber tool and cargo remain in `data.tool`/`data.cargo`.

0.2 adds `data.inventory={version:1,slots:[36 entries]}` and `data.agent` with goal,
intent, state, reason, observation snapshot, assigned workbench, display item, and
bounded failed-target memory. [Detailed agent contract](AGENT_FOUNDATIONS.md).

Scoreboards keep player identity/selection/allocation counts and controller
mode/status/cooldown/cut deadlines. `npcraft:state queue` is a saved list of `{id}`
records. The scheduler rotates one head record per tick and processes it only when
its marker is loaded and its approved owner is nearby in the Overworld. Unloaded
allocations are not deleted or omitted from allocation limits.

Initialization is gated by persistent metadata; reload does not zero IDs, items or
pause state. Agent records are initialized lazily and additively. No entity is
reclaimed merely because it cannot be found in loaded chunks.

## Scratch-state execution contract

Command storage and `#... np.tmp` scores are shared scratch. Every function chain
is synchronous, and only one autonomous controller chain is entered per tick.
Player requests are processed serially. Do not add scheduled continuations,
asynchronous work or nested autonomous dispatch without redesigning this contract.

Inventory operations snapshot authoritative slots, stage modifications, then commit
once all ingredient/capacity checks and external transfers succeed. Production
mutations are tightly restricted: only validated harvest commits remove blocks.
Crafting/drop transfers must not commit a partly modified snapshot on failure.
This is logical atomicity, not crash-proof persistence across separate save files.

## Navigation contract

Local BFS uses at most 128 temporary nodes within a six-block sphere. Each node
retains its first step. Cardinal walk, +1 full-block ascent and -1/-2 descents are
considered only with support and body clearance. The actual chosen step is checked
again immediately before movement, including overhead/drop-column sweeps. No
navigation block edits, chunk force-loading, swimming or rescue wall teleport.

Far goals use a strictly improving explored frontier with Manhattan distance in
X/Y/Z. This is not a globally complete planner. Movement remains grid-stepped, not
continuous physics; complex terrain may safely stop it. Temporary `npcraft.nav`
markers are removed at the end of each synchronous plan and on load.

## Ownership and lifetime

Public actions come from a finite trigger table. UI visibility is not authorization:
commands require approval, distance, owner ID and UUID checks. Read-only panel/status
requests and unknown action IDs do not invalidate work. Returns create public drops.

Dismissal returns backpack and legacy items first, aborts if any transfer failed,
retires the cosmetic body after clearing its display copy, removes the queue entry,
then deletes the controller. Operators who manually alter NBT/scores or copy display
equipment are outside the security model. External claim-plugin permissions are
not automatically enforced by vanilla datapack commands.
