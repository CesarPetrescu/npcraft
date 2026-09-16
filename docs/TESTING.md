# Testing and evidence

## Layers

1. `python tools/validate.py`: resource/metadata/reference checks and selected safety
   policies. This is **not** Minecraft's command parser.
2. `python -m unittest discover -s tests -v`: offline packaging, negative validation,
   installer, transport and contract tests. Test count is printed by the runner.
3. `python tools/server_test.py --accept-eula`: exact official vanilla Java 26.3,
   isolated loopback RCON, real functions/entities/items and world state. Original
   regression cases plus `tools/agent_tests.py`, including full process restarts.
4. `tools/client_playtest.py --accept-eula` and `tools/agent_playtest.py --accept-eula`:
   unmodified graphical clients under Xvfb/Mesa, keyboard/mouse player requests,
   independent RCON assertions, genuine screenshots and client/server logs.

Review Minecraft's EULA before acceptance. The harness never opens a real user
save. The official version's downloads are hash-verified; no latest-version fallback.
No binaries, accounts, server properties or worlds are committed or distributed.

## Agent assertions

Exact-component stack merging and unlike-component separation; stack caps; partial
staging rollback when full; failed recipes preserving ingredients; mixed plank
recipes; absent/destroyed workbench; mining tool/reach/plot checks; durability and
pick exhaustion; full-backpack block conservation; one-block ascent; safe two-block
and refused three-block drops; overhead and changed-landing validation; failed-target
memory; owner absence; read-only/unknown actions; additive initialization; backpack
persistence and the complete empty-inventory stone-pickaxe chain.

The new GUI scenario verifies exact before/after item records rather than assuming
one text-component serialization. Player gives/returns and goals originate through
the real client. The workbench/resources and camera are disclosed fixture setup,
not proof of natural exploration. Source/test-specific details appear in
[AGENT_FOUNDATIONS.md](AGENT_FOUNDATIONS.md) and the PR's recorded runtime evidence.

The earlier two-client timber/gallery report remains [CLIENT_PLAYTEST.md](CLIENT_PLAYTEST.md).
It is historical evidence for that scenario; it must not be relabeled as new agent
screenshots. A machine-readable report should include source SHA, run ID, assertions
and capture names. Never equate defined tests with passing tests.

## CI gates and artifacts

Unit/validation/build jobs run on Linux and Windows. Vanilla integration runs with
Java 25 on Linux. `Required` fails when a prerequisite fails, is cancelled or skipped.
The separate graphical workflow is read-only and uploads screenshots/results/logs
on success or failure. Branch protection is separate repository policy: require
both `Required` and `Vanilla GUI, player controls and screenshots` to gate them.

Tests do not upload runtime credentials, server properties, world saves or JARs.
RCON fixture writes are kept bounded; a huge command can close the connection before
a datapack function is tested. Inspect failure logs to separate transport, test
assumption and actual implementation failures; do not silently weaken assertions.

Actions are pinned to commit SHAs. No privileged `pull_request_target` workflow.
Tag publishing requires CI and exact tag/project-version agreement, but no release
is created merely by adding this configuration. The graphical gate is separate
from the tag publisher unless explicitly added to that release policy.

## Remaining manual/long-run testing

Different GUI scales/key bindings, audio/accessibility, latency and authentication,
natural terrain, multiple agents competing for shared resources, interleaved item
transfers, extended sessions and production performance remain outside the bounded
fixtures. Record this coverage separately; screenshots and short GUI scripts do not
establish smooth movement, human play quality or general survival/PvP readiness.
