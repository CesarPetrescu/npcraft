# Roadmap

Order work by acceptance evidence, not number of NPC abilities.

## M0 — current controllable timber alpha

Implement and verify the current scope, vanilla CI, artifacts, documentation and
manual two-player/UI checklist. Fix resource accounting and command failures before
adding jobs. Do not label it production-ready on the strength of static tests.

## M1 — movement and interaction quality

Smooth visible movement with swept clearance/support tests; safe one-block steps;
head orientation and walking animation evaluation; bounded cached paths; clearer
failure messages; larger obstacle fixtures; real-client tests. Keep navigation
separate from any terrain-edit permission. Benchmark one/four companions first.

Acceptance: the documented obstacle course passes with changing terrain and no
clipping, floor destruction, unsupported jumps or unbounded command chains.

## M2 — robust inventory and forestry

Multi-slot full-component item stacks, compatible-stack merging, safe player GUI,
assigned supply containers, general tool tiers/enchantments, natural-tree policy,
replanting from consumed saplings, taller bounded jobs and interruption recovery.
Design death/crash recovery and schema migration before expanding authoritative
inventory. Evaluate vanilla loot-table integration instead of hard-coded yields.

Acceptance: conservation and component-preservation tests under full storage,
concurrent users/workers, tool swaps, interruption, unload/reload and shutdown.

## M3 — real survival jobs

Supported recipes and ingredient planning; assigned real furnaces and fuel;
farming; protected bounded quarry; explicit equipment progression; hunger/health.
Do not implement free output masquerading as crafting or smelting.

## M4 — combat, dimensions and blueprints

Test mob targeting/retaliation per supported mob before claiming combat parity.
Add mortality, item-safe death/respawn, explicit portal transitions, limited mounts,
then permission/material-checked blueprint construction. Arbitrary English house
design and language-model integrations remain optional separate projects.

## Scale gate

The 16-allocation cap is not measured capacity. Record worst-case MSPT, command
counts, temporary entities, queue latency and visible movement with 1/4/8/16 workers.
Only increase caps when behavior and performance remain within an agreed budget.
