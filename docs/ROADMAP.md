# Roadmap

## Delivered

0.1: owned companions, native controls, bounded timber work, resource accounting,
vanilla integration and actual-client GUI testing.

0.2: 36-slot component-preserving backpack, validated actions, finite stone-tool
goal, failed-target memory, conservative vertical navigation.

0.3: usable-tool consistency, self-built table/furnace and native iron smelting,
finite iron/rival kits, per-controller cached routes, fast runtime work, read-only
backpack/status/plot UI, optional mortality/meals/death/recovery, consent-bound
bounded melee rivals, and full CI including graphical and multi-agent acceptance.
See current scope and test reports for exact supported behavior, not feature names.

## Remaining, not hidden inside the 0.3 claim

1. **Unified inventory/equipment:** transactional migration of legacy tool/cargo,
   armor/offhand and drag-and-drop UI. Do not remove legacy state without migration
   fixtures and full item-conservation tests.
2. **Better navigation and world knowledge:** continuous validated movement, more
   collision shapes, doors/swimming/climbing, time-budgeted incremental searches,
   longer-term observed resource maps, seed-based exploration, expiring reservations
   for contested workstations/routes. Never grant omniscient ore/player knowledge.
3. **General progression and survival:** game-data-derived supported recipes,
   quantity-aware material/fuel planning, food production, player-like survival
   mechanics and validated per-mob retaliation. This is separate from storing items.
4. **Richer rivals:** retreat cover selection, shields/bows, equipment assessment,
   difficulty/reaction parameters, factions and explicit match objectives. Consent,
   non-opponent protection, real reach/cooldowns and loss of sight remain invariants.
5. **Construction and dimensions:** material-accounted blueprints and placement
   permissions, portal policies and recovery. No arbitrary building/raid promise.

## Acceptance before expansion

Keep old GUI and accounting regressions passing. Add changing-world, contested
resource and natural-world tests. Compare multiple seeds and record blocked time,
completion rate, remaining resources, command cost and worst-case tick behavior.
Accelerated prepared plots are useful regression evidence, not natural-world proof.
A richer optional server engine can be evaluated on the same acceptance scenarios
without silently changing the vanilla installation contract.
