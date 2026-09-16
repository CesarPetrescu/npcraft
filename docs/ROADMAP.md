# Roadmap

## Delivered milestones

**0.1:** Owned companion controllers, native controls, bounded flat navigation,
timber harvesting/accounting, deterministic distribution, vanilla and real-client CI.

**0.2:** Initial 36-slot backpack transactions, validated action outcomes, a finite
stone-tool prerequisite goal, failed-target memory, conservative vertical edges,
and expanded regression/graphical scenarios. These are foundations, not full player
parity or an independent opponent. [Current contract](AGENT_FOUNDATIONS.md).

## Next: generalize one tested layer at a time

1. **Inventory and actions:** visible backpack UI, authorized equipment use, table
   construction, resource/accounting interruption tests, safe multi-worker output
   storage and explicit per-action budgets. Keep names/components intact.
2. **Broader progression:** game-data-backed recipe prerequisites; generic supported
   harvest rules; iron, fuel and actual furnace operations. Do not invent resources
   or mask unsupported enchantments with hard-coded rewards.
3. **Movement and perception:** smoother presentation, bounded cached paths, terrain
   primitives with clearance tests, incremental exploration and finite stale-aware
   resource memory. Test changing terrain, not only fixed clear plots.
4. **Survival then opponents:** health/food/death and item-safe recovery; per-mob
   combat/retaliation checks; fair player last-seen tracking, retreat and equipment
   assessment. Only then add independent rival objectives, bases and dimensions.

## Acceptance gates

An empty-backpack stone-tool fixture validates the current goal only. A later iron
milestone must obtain iron equipment from declared world resources without hidden
inventory injection. A survival milestone needs natural-terrain day/night sessions,
death/recovery and safe interruption. An opponent milestone needs two-player PvP
with legitimate reach/cooldowns and no omniscient target tracking.

Profile 1/4/8/16 workers on named hardware and report command cost, entity count,
queue latency and MSPT distributions before asserting capacity. Current allocation
caps are safeguards, not measured performance. Full survival/PvP may justify an
optional server engine, but this iteration does not add or require one.
