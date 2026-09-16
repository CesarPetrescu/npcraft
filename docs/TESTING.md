# Testing and evidence

## Required layers

| Layer | Command / fixture |
|---|---|
| Generated-runtime consistency | `python tools/generate_agent.py --check` |
| Structural/policy validation | `python tools/validate.py` (not a full command parser) |
| Offline tests | `python -m unittest discover -s tests -v` |
| Existing real-server regression | `python tools/server_test.py --accept-eula --reports reports/legacy` |
| Agent real-server acceptance | `python tools/agent_test.py --accept-eula --reports reports/agent` |
| Existing graphical / two-owner acceptance | `tools/client_playtest.py` under Xvfb |
| New graphical autonomous acceptance | `tools/agent_playtest.py` under Xvfb |

The exact committed revision's CI is the pass/fail authority. A declared test is
not evidence of execution. Counts are not coverage percentages. See AUTONOMY.md and
the captured JSON for concrete source/run provenance, and CLIENT_PLAYTEST.md for
the original worker's historical evidence.

## New agent coverage

Inventory initialization/idempotence, fixed slot count, native 16-stack limits,
full-component separation, stack merging/splitting, full and partial capacity
rollback, invalid quantities/limits/schema/length, ingredient consumption, missing
inputs, full recipe output, real workbench requirement/removal/reach, timed barehand
logs, pick gating and durability/breakage, unsupported picks, support occupancy,
block whitelist, plot bounds, stale resources, unreachable-memory bound/expiry,
resource waiting, empty-inventory stone kit, lost-sword replanning, repeated return
without duplication, and process-restart persistence.

Movement coverage: same-height detours plus one-block ascent/descent, low ceiling,
changed transition headroom, corrupted non-adjacent steps and refused two-block
falls. Existing gap/lava/unloaded/negative-coordinate fixtures remain mandatory.
No fixture gives permission for navigation to break or place a block.

## Graphical evidence

The original GUI test connects **two actual vanilla graphical clients** with separate
synthetic identities. It exercises real menu clicks, source item transfer, autonomous
legacy timber output, blocked foreign selection/control/dismissal, and reload.

The new GUI test starts one empty companion through client input. After plot/goal
assignment it calls no internal action/planner functions to drive progress. RCON
independently asserts wooden pick progression, placed workbench, final kit and
exact mined count. An explicitly injected lost sword must be replaced without a
new goal request. Produced items return to the real player's inventory. A later
named/damaged item gift tests generic backpack transfer separately. Real scheduled
Follow traverses a two-step terrace up and back down.

Scenes are controlled creative-mode fixtures. RCON positions camera and constructs
resources, not a natural survival playthrough. Brief tick freezes are only for
framing screenshots; actual progression is unfrozen. PNGs are direct framebuffers,
not generated/composited images. Software rendering is not a GPU or MSPT benchmark.
Anonymous-profile, Realms, narrator and graphics fallback messages may appear;
command/resource/macro/serialization failures are not ignored.

## Automation and artifact boundaries

Server/client downloads are exact-version official binaries verified against
Mojang metadata. All servers bind to 127.0.0.1 with disposable worlds and explicit
EULA acceptance. No account credentials or public server authentication is used.
No client/server binaries, saved worlds or credential-bearing properties are uploaded.

JUnit and server logs: reports/legacy and reports/agent. GUI JSON/screenshots and
client/server logs: reports/visual and reports/agent-visual. Diagnostics upload even
on failure. Inspect captures as well as machine-readable assertions before claiming
visual usability. Failure logs are retained, not replaced with a success picture.

CI runs offline quality on Linux and Windows. The vanilla job runs both server
suites; a reusable read-only graphical workflow runs both client suites. **Required**
combines all jobs and rejects skipped/cancelled/failed prerequisites. PRs have no
writeback/publication step. The release workflow reuses this gate and alone grants
contents-write for a tag-triggered publish job. Branch protection must require
Required separately; workflow code does not configure repository policy.

## Remaining release acceptance

Prolonged naturally generated survival sessions, arbitrary unprepared terrain,
all dialog controls with different GUI scales/key bindings, pause/unload/upgrade
under multiple active workers, all relevant item components, advanced claim plugins,
crash recovery, audio/accessibility and actual production performance need additional
work. Test 1/4/8/16 workers on documented hardware before capacity claims. A clean
short controlled test does not certify all of these.
