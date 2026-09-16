# Agent/developer handoff

Read README.md, docs/SCOPE.md, docs/ARCHITECTURE.md and docs/TESTING.md first.
This is a vanilla datapack with no build dependencies beyond Python's stdlib.
The compatibility target is **26.3 / pack 121.0 / Java 25**. Verify Mojang's primary
sources before any version change; updating the number is not a compatibility fix.

Required checks: `python tools/validate.py`, `python -m unittest discover -s tests -v`,
`python tools/build.py`, and the complete CI including vanilla, graphical and scale jobs.
Report which checks actually ran. Never describe JSON lint as a Minecraft playtest.

Critical invariants: owner ID plus UUID; owner-approved commands; no block edits
in navigation; no production forceload; one expensive planner opportunity per tick;
sequential synchronous fast-runtime chains; bounded scans/searches; item credit
only after successful block removal; remove source inventory only after successful
transfer; clear display copies before dismissal; no reclamation of unloaded records.

Do not add proprietary Marketplace material or copy a third-party GPL pathfinder
without an explicit licensing decision. Do not introduce an LLM to replace
movement/tool/action validation. Update documentation when implementation differs
from a proposed feature. Work on a branch and open a PR; do not force-push main.

## Inventory and actions

The backpack is 36 total slots, not 45. Transactions modify command-storage snapshots
before one commit. Preserve legacy timber tool/cargo during additive initialization.
Public actions are finite; status/menu/unknown requests must not reset pending work.
Navigation is full-block grid +1/-1/-2, not continuous physics. Keep movement free
of terrain edits. Never label a finite dependency controller general GOAP reasoning.

## 0.3 contract

Read docs/IRON_SURVIVAL_RIVAL.md. Shared scratch has synchronous lifetime. Cached
routes and resumable state belong to markers. Do not let visible bodies and action
positions diverge. Never copy marked visual equipment into authoritative inventory.
Preserve action42 as global epoch revocation independent of range/dimension/approval.
Native furnace contents and timers must remain real; no synthetic smelting rewards.
Never read/modify a native DYING mannequin through /data. Mortality stays opt-in.
Keep the explicit ACL byte suffix: macro interpolation strips numeric NBT types.
Run all three graphical scenarios, main/adversarial/lifecycle server cases and the
1/4/8/16-agent production-runtime soak. Accelerated fixtures are not natural-world
or human-latency benchmarks. Archive actual evidence and document remaining limits.
