# Roadmap

## Delivered foundation — 0.1

Controlled mannequin companions, stable IDs/ownership, explicit work areas, bounded
flat pathfinding, timber gathering/accounting, deterministic builds, real-server
and graphical two-client tests. Historical evidence: CLIENT_PLAYTEST.md.

## Delivered next milestone — 0.2

36-slot component-preserving backpack; staged add/take/crafting; real workbench
placement; finite raw-resource/recipe planner; empty-inventory stone-kit goal and
lost-tool replanning; bounded failed-target memory; one-full-block up/down movement
with collision/support/adjacency checks. Evidence: AUTONOMY.md.

This is **bounded progression**, not the whole autonomous-rival roadmap. The agent
is still owner-approved, nearby-owner dependent and restricted to one work plot.

## Next: stronger everyday survival primitives

Unify legacy and backpack equipment/storage with an explicit migration; safe GUI
inventory; automatic supply/output containers; wider tested tool and recipe support;
real fueled furnaces; food and sleep. Add deterministic seeded resource fixtures and
missing-input/obstruction recovery before increasing recipe count.

Navigation needs animation/smoothing and carefully tested extra primitives, not
teleport shortcuts: safe continuous clearance, vertical target approach, supported
stairs/slabs, route caching and world changes. Measure worst-case command cost and
MSPT before enlarging search budgets or companion caps.

## Then: independent survival

Persistent observed-location map, bounded exploration, resource acquisition beyond
a hand-selected plot under explicit world permissions, iron/armor progression,
health/hunger and damage. Design authoritative inventory death/drop/respawn recovery
before enabling mortality. Exact-one ownership matters more than feature count.

Acceptance: naked spawn on several seeded survival worlds completes a defined
progression without operator scene edits and survives interruptions/restarts.

## Then: a playable rival

Supported PvE target acquisition/retaliation, attack cooldown/range/line-of-sight,
retreat/heal, then opt-in player combat with non-omniscient last-seen memory, finite
reaction times and target consent/configuration. Work toward mutually contestable
goals before implementing base raids or faction building.

Acceptance: the opponent is mortal, spends real resources, has no hidden player
location feed, cannot hit through walls, and recovers sensibly after losing fights.
Dimensions, mounts, blueprint construction and broader strategic personality follow
as separately tested systems, not labels on an unfinished implementation.

## Scale and release gate

Current caps (4 per owner / 16 allocated globally) are safety settings, not a
benchmark. Record hardware, median/p95/p99 MSPT, planner cost, queue latency and
entity count for 1/4/8/16 active workers, including blocked searches. Larger caps and
production readiness require those measurements and prolonged multiplayer tests.
