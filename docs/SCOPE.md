# Scope and acceptance criteria

## 0.2.0-alpha.1

Build useful vanilla companions with explicit ownership, permitted work areas,
resource conservation and safe failure behavior. This milestone is a bounded
agent foundation, **not a full survival or PvP player**.

The original timber worker remains: oak/birch logs in a 7 x 7 x 4 plot, given iron
axe, single-type legacy cargo and empty-slot barrel deposits. New agent mode adds a
36-slot full-component backpack, validated mine/craft actions, a finite stone-pickaxe
prerequisite goal, expiring failed-target memory and full-block vertical navigation.

The goal starts with an empty backpack/no mining tool, given an allowed plot with
logs and exposed stone plus a reachable real assigned crafting table. It obtains
a wooden pick, mines three cobblestone, then crafts a stone pick with actual input
consumption. It does not construct its own table or discover arbitrary recipes.

Navigation supports cardinal full-block walking, one-block ascent, and one/two-block
descent. It remains grid-stepped. It never grants permission to break/place blocks,
load chunks, jump unsafe gaps or ignore overhead/landing clearance.

## Hard boundaries

- Vanilla Java 26.3 / pack format 121.0; no speculative version compatibility.
- Original code, no paid Marketplace assets or copied third-party pathfinder.
- Operator approval, numeric owner plus UUID authorization and distance checks.
- Stop autonomous work without an approved nearby owner in the Overworld.
- Revalidate action bounds, target, reach, tool, ingredients and inventory capacity.
- Commit item changes only after all checks and external transfer successes.
- Preserve existing schema-1 ownership, tool/cargo and allocation state on upgrade.

## Acceptance evidence

Require structural/unit checks, actual vanilla-server regression tests, and both
unmodified-client GUI scenarios. Tests must check positive progress and negative
cases: insufficient capacity/ingredients, missing workbench, unsafe movement,
blocked targets, stale data, unauthorized requests, cancellation, reload and full
process restart. The complete resource balance is in [AGENT_FOUNDATIONS.md](AGENT_FOUNDATIONS.md).

Runtime tests are not a percentage of all Minecraft behavior. Screenshots are not
performance measurements. Both success and remaining unsupported cases must be
reported. Keep releases experimental until broader playtesting is recorded.

## Not delivered

Independent offline rivals, health/hunger/death recovery, PvP/combat, ore/smelting
progression, general recipe planning, inventory GUI/equipment parity, natural cave
exploration, swimming/slabs/stair-shaped blocks, doors/mounts/portals, autonomous base
building and general long-term world/opponent memory. See [ROADMAP.md](ROADMAP.md).
