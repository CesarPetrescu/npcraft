# Agent/developer handoff

Read README.md, docs/SCOPE.md, docs/ARCHITECTURE.md and docs/TESTING.md first.
This is a vanilla datapack with no build dependencies beyond Python's stdlib.
The compatibility target is **26.3 / pack 121.0 / Java 25**. Verify Mojang's primary
sources before any version change; updating the number is not a compatibility fix.

Required checks: `python tools/validate.py`, `python -m unittest discover -s tests -v`,
`python tools/build.py`, and the vanilla CI job. Report which checks actually ran.
Never describe JSON lint or a Python model as a Minecraft playtest.

Critical invariants: owner ID plus UUID; owner-approved commands; no block edits
in navigation; no production forceload; one synchronous autonomous controller
chain per tick; bounded scans/searches; item credit only after successful block
removal; remove source inventory only after successful transfer; clear the visual
axe before dismissal; no reclamation of possibly unloaded controllers.

Do not add proprietary Marketplace material or copy a third-party GPL pathfinder
without an explicit licensing decision. Do not introduce an LLM to replace
movement/tool/action validation. Update documentation when implementation differs
from a proposed feature. Work on a branch and open a PR; do not force-push main.

## 0.2 invariants
Read docs/AGENT_FOUNDATIONS.md as the current extension contract. The backpack is
36 total slots, not 45. Transactions modify command-storage snapshots before one
commit. Preserve the legacy timber tool/cargo during lazy additive initialization.
Public actions are finite; status/menu/unknown requests must not reset pending work.
Navigation is full-block grid +1/-1/-2, not continuous physics. Keep movement free
of terrain edits. Run both graphical scenarios and all real-server agent cases.
Never label the finite stone-pickaxe dependency controller general GOAP or PvP AI.
