# Testing and evidence

## Layers

1. `tools/validate.py`: JSON/metadata/resource references, macro prefixes, singular
   paths and selected safety-policy checks. This is **not a Brigadier parser**.
2. `python -m unittest discover -s tests -v`: offline tests for lint rejections,
   deterministic ZIPs, checksums, pack layout, core contracts and RCON transport.
3. `tools/server_test.py --accept-eula`: boots official vanilla Java 26.3, executes
   real functions via loopback RCON and verifies state. Uses an isolated temporary
   world, not mocks of Minecraft's command implementation. It saves/restarts too.
4. Manual client/multiplayer playtesting: visual/UI quality and real player flows.

The current offline suite contains 25 tests; the vanilla suite defines 22 cases.
Numbers alone are not coverage percentages. CI's current run is the authority on
pass/fail, not this document. Never call an unexecuted test a passing test.

## Vanilla assertions

Native mannequin creation/equipment; reload-safe IDs and pause state; wall detours;
far goals; refusal to cross unsupported gaps/lava/unloaded chunks/different heights;
plot scan and delayed harvest; stale targets; positive/negative-coordinate bounds;
missing axe; full and mixed cargo; line-of-sight refusal; full barrel, successful
empty-slot transfer and no repeat credit; missing barrel; axe breakage; single
item returns; rejection without an authorized actor; pause without an online owner;
fair queue rotation; negative-coordinate navigation; dismissal without extra drops or
serialization warnings; persisted record/UUID/cargo/scores across process restart.

The headless suite does **not** log in a real player. It tests authorization
rejection, not every successful player UI/authentication path. It tests shared core
functions directly; it does not certify unexercised macro branches or client packet
handling. Missing/invalid functions and logged macro expansion failures are fatal.

Reports: `reports/vanilla.xml` and `reports/server-*.log`. GitHub uploads these even
when a test fails. It never uploads world saves, RCON passwords/properties or the
Mojang server JAR. Do not paste sensitive live-server logs into public issues.

## Manual release checklist — must be performed, not assumed

- New 26.3 client/world; install the **built ZIP**, `/reload`, check enabled packs.
- G and pause-menu dialogs open; every button works without operator privileges
  after approval. Escape/Close always exits; invalid trigger numbers grant nothing.
- Recruit four; reject a fifth. Select the nearest **owned** companion.
- Two real users: A cannot select, control, equip, dismiss or collect B's stored
  inventory via NPCraft commands. UUID ownership survives reconnect and restart.
- Give a damaged/named iron axe; return it unchanged before harvesting. Reject
  enchanted/unbreakable/nonstandard axes. Never duplicate the player-held item.
- Owner moving away, revocation, unloaded chunks, and dimension changes pause work.
- Timber demo: partial/full loads, changing species, full/broken/moved barrel,
  partial tree above the four-block plot, and an out-of-bounds player building.
- Clear a support block during movement: stop without digging, bridging or falling.
- Dismiss while loaded; collect one real axe/cargo load, no display-copy duplication.
- Measure MSPT and visible pacing with 1, 4, 8, 16 companions on named hardware.
  Record p50/p95/p99 and worst-case blocked-route searches. No capacity claims before
  this benchmark. Record the intentionally grid-stepped movement on video.

## CI security and release gate

Actions are pinned to full commit SHAs and monitored by Dependabot. PR jobs have
read-only repository permissions, do not persist checkout credentials, and run no
`pull_request_target` or secret-bearing untrusted-code workflow. The publisher's
write permission exists only in the tag-triggered publish job after CI.

The exact version is resolved from Mojang's manifest, with no `latest` fallback.
Java 25 is explicit. Tag `v<project version>` must match project.json. Archive
contents are generated solely from datapack resources. The Required job treats
skipped/cancelled dependencies as failures. Branch protection must separately
require **Required**; workflows alone do not configure repository policy.
