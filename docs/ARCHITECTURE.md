# Architecture

```text
Native dialog / trigger request
  -> approval + dimension + range
  -> owner ID AND stored player UUID
  -> persistent marker controller + finite mode
  -> saved fair queue (one allocated record per tick)
     -> nearby approved owner + cooldown
     -> legacy worker OR autonomous dependency planner
        -> bounded perception / remembered failed targets
        -> navigation primitives
        -> validated action + staged inventory transaction
  -> mannequin presentation sync
```

## Persistence and separation

Root schema 1, `npcraft:state queue`, IDs and legacy records remain unchanged.
Controllers are `minecraft:marker`, tag `npcraft.bot`; the paired mannequin has
`npcraft.body` and the same `np.id`. It is invulnerable, not an independently
simulated player. Only the marker holds authoritative item records.

Player scores: `np.owner`, `np.sel`, `np.count`, `npcraft` trigger. Controller scores
include ID, owner, mode, status, next-work tick, cutting deadline and legacy harvest
count. Mode 0 stay, 1 follow, 2 home, 3 legacy timber, **4 autonomous stone kit**.
The saved queue rotates one `{id}` per tick, including unloaded allocations, to
avoid starvation and unsafe reclamation. Never infer deletion from absence.

New lazy module:

```text
data.agent.schema = 1
  bag: 36 cells, either {} or {item: full vanilla item stack, max: native limit}
  hand: cosmetic copy selected from bag; not another owned item
  equipped: selected slot index
  goal: stone_kit
  task: current task or explicit waiting reason
  resource: current required raw resource
  target: optional {x,y,z,kind}
  station: optional {x,y,z}, must still be an actual reachable workbench
  scan / scanned: bounded plot search cursor/progress
  blocked: at most 16 failed targets
  forget_at: next failed-target-memory expiry
  failures: consecutive blocked attempts at the selected target
  crafted / mined: diagnostic counters, not sources of resources
```

The 36 slots include nine hotbar-equivalent slots; no separate 9-slot duplication.
Legacy `data.tool` and `data.cargo` remain independent and are not implicitly moved.
Public give/return commands distinguish backpack versus legacy storage. Dismissal
returns all three real stores, retires the cosmetic body, then deletes the record.

## Execution and transactions

Global scratch storage and temporary scoreboard values are safe only under the
existing synchronous command-chain contract. One autonomous controller chain runs
per tick; player requests also complete serially. Never introduce async callbacks,
scheduled continuations or reentrant inventory operations without changing this.

`inventory/begin` validates module schema and exact bag length, marks staging ready,
and copies the current bag. `add_staged` merges only identical complete item data
apart from count, respecting stored/native limits, then fills empty slots.
`take_staged` consumes recipe ingredients on that copy. A caller publishes the copy
only after the **entire** operation succeeds. Insufficient capacity/ingredients
leaves authoritative inventory unchanged, including partial-merge failures.

A held-item transfer obtains full SelectedItem and native max-stack limit, stages
capacity, removes the source hand only on success, then commits. Ordinary return
summons a full item stack and clears its source cell only if summon succeeds.
Existing nondefault components are not replaced by a simplified ID/count pair.

These are synchronous logical transactions, not cross-region crash-proof database
transactions. Power/process failure or mixing partial world backups can break
persistence consistency. Use whole-world backups and clean server shutdowns.

## Action API and trust boundaries

Agent action functions are internal implementation, not an arbitrary public command
API. The public interface is the finite owner-checked trigger table. Operators
can still edit NBT or call internal functions; protecting against the world owner
with operator privileges is outside the model.

Mining validates loaded Overworld, plot bounds, exact supported block, occupied
support underneath bodies/players, reach, line of sight, correct usable tool, and
output capacity. Timed oak gathering permits bare hands; stone requires supported
wooden/stone pick. Stage output -> revalidate -> remove one block -> credit one
supported drop -> wear tool once. Another actor removing the block first produces
no output. No general loot-table/enchantment parity is claimed.

Workbenches are real blocks placed with `keep` at the explicitly permitted empty
center, from a consumed item. Occupancy/headroom/support/reach are checked. Other
blocks are never overwritten for convenience. Station-based recipes validate the
recorded block, distance and line of sight; a missing station is replanned.

## Planner and perception

`tools/generate_agent.py` is the reviewed source for the generated agent runtime.
It compiles eight recipes and their finite prerequisite calls. All generated files
are committed; build/CI verifies drift. Python never executes in Minecraft.

The planner checks actual inventory each visit in a fixed priority order: usable
stone pick, stone sword, stone axe, furnace. Missing ingredients recursively select
one leaf action, with a workbench dependency for 3x3 recipes. This is an intentionally
small acyclic task planner, not dynamic utility scoring, GOAP or an LLM.

A job scans at most eight of 196 authorized positions per visit. After three failed
attempts, it remembers a target and tries another. Memory holds at most 16 entries
and expires after 400 game ticks so changed terrain can be retried. Missing resources
and full inventory back off. It does not know resources outside the plot or the
opponent's location. Loss of supported equipment is detected by later inventory
checks, not by a new player order.

## Navigation

The existing BFS still bounds insertion to 128 nodes within a six-block local
sphere, and carries only the first step of a path. A far goal may choose a strictly
improving explored frontier; this is not a globally complete route planner.

Each cardinal edge can stay level, rise one full block, or drop one full block.
Loaded destination, support floor, feet/head clearance and extra transition
headroom are required. Execution rechecks source/destination, Manhattan adjacency,
height delta and sweep headroom after planning. The body then moves one grid step.
This is not continuous player physics or animation, and does not support stairs,
slabs, gap-jumping, swimming, climbing or arbitrary falls.

Navigation has no terrain mutation permissions. Mining support is also refused
while a player/companion occupies it. The root goal must be reached at the requested
Y level; merely standing on top of a mining target is not arrival.
