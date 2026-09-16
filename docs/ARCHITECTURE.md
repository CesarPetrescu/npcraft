# Architecture — 0.3

```text
player trigger/dialog -> approval / UUID / range -> owned controller
     | action42: global consent revocation before ordinary locality checks
     v
persistent marker: inventory, legacy items, goal, route, survival, rival epoch
     |
     +-> fast synchronous pass (up to16): death/food, consent, vision, cached motion
     +-> fair one-record slow queue: prerequisites, local BFS, work/actions
     |
     v
validated native world/item operations -> mannequin presentation sync
```

The controller marker owns all items and persistent decisions. Native mannequin
Health is authoritative only after mortality is enabled; equipment on it is a
marked presentation copy. Losing a body produces a persistent tombstone, real item
drops, and a safe empty respawn—not reconstruction from a stale inventory copy.

Scoreboards hold IDs/modes/deadlines; marker `data` holds structured records.
`npcraft:state` stores the round-robin allocation queue, owner ACL and consent
epochs. IDs are not recycled on reload. New records initialize additively, retaining
the old timber tool/cargo and all36 agent slots. Unloaded allocations remain counted.

Function chains are synchronous. Each planner/inventory operation resets and uses
shared scratch within that call only. Future multi-tick planning must persist its
continuation state on the controller; do not put it in shared temporary storage.
Inventory mutations stage a full snapshot, validate capacity and external success,
then commit. Workstations and supported block edits have separate permission checks;
pathfinding never inherits a mining/construction permission.

Local bounded BFS produces per-controller route steps. Fast execution revalidates
support, clearance, edge height, occupancy and optional arena constraints. A changed
route or next cell clears the cache. Global graph completeness, mutual-agent
reservation protocols and smooth continuous physics are not implemented.

Rivals use an explicit UUID opponent and persistent consent epoch, not nearest
player targeting. Only line-of-sight observations enter last-seen memory. Attacks
have independent consent/reach/LOS/cooldown checks even if a planner is stale.
The global withdrawal action is permitted even when the owner moves dimensions or
loses ordinary control range; unloaded rivals cannot retain permission indefinitely.

See [full record/lifecycle contract](IRON_SURVIVAL_RIVAL.md), [operations](OPERATIONS.md)
and [testing](TESTING.md). Logical transactions do not make Minecraft's separate
save files a crash-proof database; use complete consistent backups.
