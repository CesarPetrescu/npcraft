# Agent / developer handoff

Read README.md, docs/SCOPE.md, docs/ARCHITECTURE.md, docs/AUTONOMY.md and
TESTING.md before changing behavior. Target: **Java 26.3 / pack 121.0 / Java 25**.
Verify official technical sources and exact-version tests for any version upgrade.

Required offline checks:

```sh
python tools/generate_agent.py --check
python tools/validate.py
python -m unittest discover -s tests -v
python tools/build.py
```

Agent resources are generated from `tools/generate_agent.py`: edit the generator,
regenerate and commit both. The package must run with only the committed datapack,
without a development script or external process. Existing core/navigation files
are directly maintained. Root schema and legacy inventory must survive upgrades.

Required runtime evidence: both server_test.py and agent_test.py; both graphical
client_playtest.py and agent_playtest.py on a Java25/Xvfb/Mesa runner. Report checks
actually executed. JSON lint is not Minecraft command parsing; screenshot capture
is not proof of broad survival behavior. Never manufacture a screenshot/result.

Invariants: finite owner-checked trigger API; owner ID AND UUID; no navigation block
edits or forced loading; one synchronous autonomous chain per tick; staged backpack
transactions; credit only after block removal succeeds; source deletion only after
successful transfer; capacity and full item components preserved; clear display
copies before retirement. No reclaiming possibly unloaded NPCs.

The autonomous agent is a **finite stone-kit dependency planner**, not a complete
GOAP/utility AI or PvP system. Bodies remain invulnerable. Inventory has 36 slots
including the nine hotbar equivalents, separate from legacy cargo/tool. Movement
is grid-based single-block steps, not complete player physics. Keep scope honest.

Work on a branch, add real regression fixtures, retain read-only PR CI, and do not
merge or tag releases without instruction. No proprietary Marketplace material,
server/client binaries, world saves, private account tokens or credentials committed.
