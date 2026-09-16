# Scope and acceptance criteria

## Product goal

Make a small group of useful, controllable Java companions—not fake connected
players and not “generative AI.” Explicit ownership, designated work areas,
conserved resources and recoverable failures take priority over feature count.

## 0.1.0-alpha.1: implemented vertical slice

The code implements a mannequin presentation layer over persistent marker records,
operator approval, owner-checked trigger controls, native dialogs, a fair one-record
per-tick scheduler, bounded flat-ground navigation, and an oak/birch timber job.
The README is the player-facing feature contract. CI is the executable gate for
these implementations; visual/client usability is a separate manual requirement.

### Hard constraints

- Pure vanilla datapack; no client mod, mandatory resource pack or external AI.
- Exact Minecraft 26.3 target, pack format 121.0; no untested compatibility claims.
- No copied Gamemode One assets/code, no bundled GPL pathfinding dependency.
- No navigation-driven block destruction, block placement or forced chunk loading.
- Only an approved owner can issue player-facing mutations. UUID and numeric owner
  checks are both required; menu visibility is not authorization.
- All world mutation must revalidate plot bounds and target type. All item transfer
  must confirm success before removing the source record.
- Pause when the owner is offline, revoked, outside 64 blocks, or in another dimension.

### Actual gameplay boundaries

Movement is at a single integer Y level, centered on full-block cells. Two air-like
body cells and a conservative support-block allowlist are required. Navigation is
cardinal, grid-stepped, not a general physics/collision engine. It cannot step over
slabs, jump, climb stairs, swim, open doors, or cross portals. Far-goal frontier
selection can stall at complex concave obstacles; it must stop rather than dig.

A timber plot is X/Z ±3, Y +0..+3. All ordinary oak/birch logs inside are eligible,
including player-placed logs. Leaves, saplings, other log species, stripped logs and
logs above the plot are untouched. The supported plain-log yield is explicitly
one log per successful removal; overridden loot tables are not evaluated. No
replanting, general tree recognition, self-crafted tools or autonomous progression.

The inventory is one stack (at most 64 logs of one species) plus a real iron axe.
The axe must be unenchanted, breakable and have standard 250 durability. Custom
name and existing damage are preserved. General enchanted-tool semantics are not
implemented. Barrels are explicitly assigned; only empty slots are written.

Mannequin bodies are invulnerable and their held axe is a presentation copy.
Normal survival combat/death and arbitrary armor/inventory management are out of
scope until accounting and recovery can be redesigned and tested for death.

## Definition of done for this alpha

CI must parse the pack in the exact vanilla server, reject broken function/resource
loads and expanded macros, and pass behavioral assertions for navigation, hazards,
plot bounds, timed cutting, axe wear, stale targets, stack limits, blocked storage,
authorization rejection, queue rotation, reload and restart persistence. The ZIP
must be deterministic, directly installable and contain no development/server data.

A release candidate also requires a recorded manual client session for dialogs,
selection, visual movement, non-operator tool transfers and two-player ownership.
Headless tests do not certify these client-facing behaviors or production capacity.

## Deferred, not silently promised

See ROADMAP.md for smooth/vertical movement, robust multi-slot inventory, resource
progression, forestry, combat/death, dimensions, mounts and blueprint construction.
Twenty companions is a future measured capacity goal, not an inherited requirement
from a different add-on's marketing.
