# Changelog

## 0.3.0-alpha.1 — unreleased

Self-built table/furnace iron progression; native fuel/smelting; shared usable-tool
selection with descriptive metadata; cached routes and a separate fast runtime;
read-only backpack/status and plot preview; opt-in mortality, simplified meals,
single-drop death/safe empty respawn/marked-loot recovery; consent-bound bounded
melee rivals with last-seen memory, cooldowns and retreat. Required and tag release
validation now include graphical acceptance and multi-agent progression.

Execution-driven fixes: preserve byte-typed administrative ACL through macros;
expire mortal mannequin corpses without invalid DYING-pose save errors; refuse
food use on dead controllers. Regression suites cover cached-route obstruction,
loot recovery across restart, station contention/capacity and normal health/damage.
The multi-agent fixture calls the normal mortality initializer before rival work.
Precise supported behavior and remaining limits are in docs/SCOPE.md.

## 0.2.0-alpha.1 — unreleased

Additive 36-slot full-component backpack with transactional transfers and recipes;
closed validated mining/crafting actions; finite autonomous stone-pickaxe goal;
short-lived failed-target memory; one-block up/two-block down grid traversal with
swept clearance checks; owner controls and cancellation; expanded vanilla and
graphical-client acceptance tests. Legacy timber workflow remains supported.

No general survival/PvP, continuous movement, unrestricted mining or general recipe
discovery is claimed. See docs/AGENT_FOUNDATIONS.md and the executed CI evidence.

## 0.1.0-alpha.1 — unreleased

Initial original vanilla datapack implementation: mannequin companions; persistent
marker records and IDs; operator-approved, UUID-checked controls; native dialogs;
fair bounded scheduling; conservative flat-ground local navigation; timed oak/birch
log harvesting in a designated plot; real iron-axe wear; single-type cargo and
empty-slot barrel deposits; item-safe normal dismissal; pause/reload support.

Development support: strict structural checks, offline regression/mutation tests,
real vanilla-server integration harness, deterministic ZIP/checksum builds,
Linux/Windows quality jobs, Java 25 runtime CI, diagnostics artifacts, release
gating, Dependabot, README, scope, architecture, roadmap and operations guidance.
