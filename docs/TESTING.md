# Verification and evidence

## Executable layers

| Layer | Command / implementation |
|---|---|
| Structure | `python tools/validate.py`: metadata, references and selected command policies; NOT Minecraft's parser. |
| Offline tests | `python -m unittest discover -s tests -v`: packaging, negative checks, installer, transport and source invariants. |
| Native main suite | `python tools/server_test.py --accept-eula`: exact official vanilla server, actual functions/world/entities, including process restarts. |
| Adversarial | `tools/v03_adversarial_tests.py --accept-eula --reports reports/adversarial`: shared resources, station/capacity rejection, migration and persistence. |
| Lifecycle | `tools/reliability_tests.py --accept-eula --reports reports/reliability`: real ACL writer types, live mortal bodies, changed cached routes, readiness, dead-food refusal and loot recovery/restart. |
| Graphical | `tools/client_playtest.py`, `tools/agent_playtest.py`, `tools/rival_playtest.py`: unmodified clients, real keyboard/mouse requests, independent RCON assertions and PNG captures. |
| Multi-agent | `tools/soak_test.py --accept-eula --agents 1,4,8,16 --ticks 6000`: production runtime/scheduler in declared loaded fixtures, no online player or per-action driver. |

Review the Minecraft EULA before explicit acceptance. Tests create isolated
loopback-only worlds and verify official downloads. They never use an existing
user world. Test-only chunk loading and fixture commands are not distributed in
the production datapack. No binaries, credentials or server properties are uploaded.

## What counts as evidence

Only completed runs establish pass/fail. A test definition or a source-string check
is not a Minecraft playtest. Report exact source SHA and per-suite assertions;
counts are not a percentage of all game behavior. Historical screenshots retain
their version provenance. The rival GUI scenario begins with declared resource
blocks, no granted stations/tools/ingots. Food is supplied separately for survival.
The actual client provides requests; RCON builds the fixture and verifies results.

Multi-agent scenarios use `tick sprint` to accelerate 6000 game ticks at each size.
They check kit completion and exact harvest accounting with production scheduling.
Their tick-query timing is software-runner diagnostic data, NOT human-latency,
natural-world, GPU, p95 server capacity or a one-hour uninterrupted session claim.
No conclusion is drawn from an allocated cap alone.

## Gates and diagnostics

`Required` fails unless Linux/Windows quality, all vanilla suites, graphical scenarios
and all four multi-agent cases succeed. The tag publisher reuses this aggregate.
All maintained test jobs have read-only repository permissions; actions are pinned
to full SHAs. No `pull_request_target`. Branch protection is configured separately;
this PR does not change repository policy or publish a release.

JUnit and isolated server logs upload even on failure. Graphical and multi-agent
JSON reports include source/run provenance and scenario state; PNGs are direct
captures, never generated or retouched. Screenshots do not establish smooth motion.
A stopped RCON transport is not automatically a datapack crash; diagnose server logs
and preserve failures instead of weakening unrelated assertions.

## Remaining validation

Natural terrain across seeds, audio/accessibility and other GUI scales, public
server authentication/latency, mobs targeting mannequins, arbitrary enchantments,
multi-hour sessions, station deadlocks in dense crowds, abrupt cross-file save
failure, and real hardware capacity distributions remain separate work. A passing
release gate certifies the declared scenarios only.
