# Scope: 0.3.0-alpha.1

The target is original vanilla Java 26.3 / pack 121.0. This release is a **bounded
progression and melee-rival prototype**, not a complete Minecraft survival player.
The full implementation contract is [IRON_SURVIVAL_RIVAL.md](IRON_SURVIVAL_RIVAL.md).

## Implemented

The inherited companion/timber/stone-goal features remain. Added: shared usable-tool
checks; self-crafted/placed table and furnace; native iron smelting with real fuel;
finite iron-pickaxe and rival-kit goals; per-controller cached routes and split
runtime/planning; native read-only backpack view and status/plot tools; opted-in
mortality, supplied-food healing, single-drop death, safe empty respawn and actual
loot recovery; explicit consent-bound melee rival within a declared home arena.

Normal work requires an approved nearby owner. Loaded rivals may think without
owner proximity only with matching persistent consent and administrative approval.
No unloaded terrain is simulated and no chunks are force-loaded. Work and station
placement remain inside the assigned 7x7x4 plot; navigation never edits terrain.

All item actions must preserve full component records, check capacity/ingredients,
validate current world state and clear sources only after successful transfer.
The legacy timber inventory remains separate; upgrade does not discard it. Native
body health is authoritative. A visual equipment copy must never become real loot.

## Acceptance gates

Quality checks on Windows/Linux; actual vanilla regression, adversarial and lifecycle
suites; three graphical-client scenarios; 1/4/8/16-agent accelerated production runs.
The release workflow requires all layers. Tests must verify successful progress AND
negative cases, not just load resources or print expected results. Record exact
source SHA, reports, direct game captures and the final artifact checksum.

The iron scenario starts empty without supplied workstations. Food is a separately
disclosed combat fixture supply. Rival tests verify actual player damage, weapon
wear, revoked consent, occlusion, death and empty respawn. Multi-agent fixtures
verify resource accounting while real production tick/scheduler logic runs.

## Not claimed

General utility/GOAP/LLM planning; arbitrary generated-world exploration; continuous
player movement/physics, parkour, swimming, doors, slab/stair-shaped traversal;
complete hunger/saturation/armor/offhand/bow/PvE parity; autonomous food production;
unrestricted PvP/factions/raiding; structures beyond workstations; portals/dimensions;
drag-and-drop backpack GUI; seamless migration to one unified legacy/backpack store;
crash-proof transactions; natural-world multi-hour performance certification.

A finite passing fixture is not proof these omitted capabilities work. See the
roadmap for separately testable deliverables rather than silently expanding scope.
