# Iron progression, mortality and rival prototype — 0.3.0-alpha.1

## Scope contract

This release extends the original **vanilla Java 26.3 / pack 121.0** datapack.
It is a finite progression and bounded melee-opponent prototype. It is not a
complete autonomous survival player, generalized planner, physics implementation,
or a claim that all items, terrain, recipes and dimensions work.

## Implemented progression

An owner assigns a permitted 7 x 7 x 4 resource volume and starts the iron goal.
With no inventory, tools, table or furnace supplied, the controller can:

1. Harvest supported logs by hand and craft planks/sticks.
2. Craft a crafting table from four planks and place it in a safe permitted cell.
3. Craft wooden and stone picks with actual ingredient/tool consumption.
4. Acquire eight cobblestone, craft and place a furnace.
5. Mine raw iron with a supported stone-or-better pick and coal with a usable pick.
6. Put actual raw iron and coal into the native furnace, wait for native cooking,
   collect actual output and craft an iron pickaxe.
7. In rival mode, acquire two additional ingots and craft an iron sword.

The existing stone-pickaxe goal remains available and keeps its old assigned-table
contract. The iron goal supplies the new self-built-workstation path. Mine actions
use a reachable visible target when already in reach; otherwise they route toward
its X/Z on the declared work floor. This is not a general arbitrary-cave standing
position solver. All mining commits revalidate type, chunk, plot, tool tier, reach,
line of sight, own support, and staged output capacity.

Only explicitly supported logs, stone/cobblestone, coal ore and iron ore (including
supported deepslate ore variants) are handled. Drops/recipes are finite rules, not
arbitrary custom loot-table/recipe discovery. The source functions are the precise
supported set. There is no diamond/netherite progression, charcoal, automatic fuel
selection, workstation GUI operation, or unrestricted construction.

Station placement consumes one actual inventory item only after successful world
placement. It tests four neighboring cells and their one-level-lower alternatives;
it cannot replace a building, entity or obstructed block. Furnace records include
a normalized native name marker; a normal replacement furnace is not silently
looted. An operator who forges the marker is outside the trust model. A foreign
input, fuel or output blocks work without overwriting it. Full backpack preserves
native output. Fuel already burning and input/output already in the furnace count
as available processing resources; a missing result is never conjured into inventory.

## Inventory, equipment and UI

The 36-slot backpack remains the authoritative agent store. It preserves complete
item components and keeps unlike stacks separate. Transfers and recipes operate
on synchronous snapshots and commit only after preconditions/external writes
succeed. This is not a crash-proof database transaction across Minecraft save files.

Tool readiness and display selection share usable-tier checks. Supported plain
wooden/stone/iron picks and swords may keep descriptive name, item name, lore and
custom data; behavior-changing enchantments/unbreakable/custom attributes are not
silently treated as vanilla. Goal completion requires a usable tool, not just an
item ID. Mining/attacking wears the actual inventory slot. Presentation items have
a reserved `minecraft:custom_data.npcraft_visual` flag and are never authoritative.

The old timber axe/cargo fields remain separate for save compatibility. This is
**not** a seamless inventory migration or a full armor/offhand manager. Do not
claim that storing an item means the AI understands how to use it.

New UI: read-only native backpack list, compact status snapshot, and a bounded
one-shot particle outline of the permitted plot. These views do not cancel work.
The inventory view is not a drag-and-drop container GUI. Returns are public drops.

## Planning and scheduling

The goal controller is a finite auditable dependency graph: observe current
resources, choose a missing prerequisite, dispatch a supported action, observe
again. It preserves a task across updates and invalidates changed targets. It is
not a general utility solver, GOAP search, learner or language model.

One allocated controller per tick receives the expensive planner opportunity.
A separate fast pass services up to the allocation cap of 16 loaded controllers
for mortality, consent, perception and following cached steps. Every function
chain remains synchronous; shared scratch storage must not survive a yield or
be used by nested interleaved agents. Persistent route steps live on EACH marker,
not global scratch. A changed destination or failed step discards that route.

The pathfinder remains bounded BFS (128 nodes, about six-block local sphere,
maximum 31-edge retained path). It supports cardinal full-block walk, +1 ascent,
-1/-2 descent and validates the exact next step before movement. Occupied cells,
unsupported floor, clearance failures and arena violations stop movement. It does
not guarantee deadlock-free multi-agent coordination or global path completeness.
Movement is discrete, not smooth continuous player locomotion or jump physics.

## Mortality, meals and death recovery

Mortality is **explicit opt-in** through action 35 or rival acceptance. Normal
companions retain their prior invulnerable mode until opted in. Native mannequin
Health and incoming damage are authoritative; there is no second custom HP bar
applying the same injury twice. NoGravity/immovable presentation means this is NOT
full player fall/knockback/water physics or certified per-mob retaliation.

The supplementary food meter is deliberately simple: maximum 20, decrease by one
per 1,200 active game ticks. Supported supplies are cooked beef (+8), bread (+5),
apple (+4). A consumed meal heals two native health points up to 20 and has an
80-tick cooldown. Food is supplied; hunting/farming, saturation, exhaustion and
vanilla food parity are not implemented. Empty-meter damage is non-lethal at one
health point. Loaded mortal agents may need supplies even when their owner leaves.

A lethal native hit creates a persistent controller tombstone BEFORE authoritative
item drops. Each stack is cleared only after its real item entity is created;
failed transfers retry. Native display-copy drops are marked and removed. The
controller cannot synthesize replacement gear. The body is prepared with a native
DeathTime of 19 while alive so its cosmetic corpse expires on the next native
entity tick; the code never serializes a DYING mannequin via /data. Runtime tests
must establish that this neither kills healthy bodies nor grants invulnerability,
and that post-death saves/restarts preserve a single inventory drop.

After at least 200 ticks, an empty replacement body can spawn at a loaded safe
home; an obstructed/unloaded home waits. A 400-tick recovery window targets the
recorded death location and can collect nearby marked real drops. Stolen, burned,
despawned or unreachable items are not recreated. Loot is public, not protected
private property; native item merging/third-party modifications are not an
ownership guarantee. No chunks are force-loaded for recovery.

## Rival mode and consent

Rival acceptance requires the **owning player** in Survival or Adventure, explicit
operator approval, and a configured work plot. Other players are never chosen as
opponents. The arena is centered on home (X/Z +/-16, Y +/-8). The resource workplot
remains independently bounded. No unrestricted raid/grief capability is granted.

The controller stores the opponent UUID and a unique consent epoch. Every active
rival checks persistent owner ACL and matching consent token. Action **42** removes
the owner's consent from any distance/dimension, even while globally paused or
after access revocation; it also stops loaded owned rivals. A new consent cannot
reactivate an older unloaded opponent with a stale epoch. Normal mode changes
stop that companion's rival mode. Operator direct NBT/function manipulation is
outside the player authorization boundary.

While loaded and authorized, rival thinking does not require owner proximity.
Unloaded regions are not simulated, and no mined resources are credited offline.
Consent does not make the opponent's hidden position available to the planner.
Sensing is bounded to 16 blocks and arena membership with line of sight; only then
is the visible position stored. Last-seen memory expires after 100 ticks. An
occluded target's live position must not refresh it. This is a line-of-sight sensor,
not a simulated human field-of-view/vision cone.

A supported sword is needed to attack. The action rechecks consent, opponent UUID,
Survival/Adventure, arena, line of sight and 2.8-block reach. Successful native
hits consume durability and respect a 20-tick cooldown. Low health (<=6) enters a
simple return-home retreat and blocks attacks until health recovers to >=14.
This is not advanced strafing, shields, bows, tactical cover selection, armor
assessment, factions or full vanilla PvP parity. Player death ends the duel.

## Release and evidence boundaries

`Required` now includes Linux/Windows quality, real-server integration, ALL
three graphical scenarios and 1/4/8/16-agent accelerated progression. The tag publisher reuses this CI, including the GUI
suite. Repository branch protection still needs the Required check configured
separately; workflows do not change repository rules. No release is created by
this PR itself.

The code defines regression assertions; only executed run artifacts establish
results. Graphical tests use the unmodified client and real input in a disclosed
creative fixture, then Survival combat. RCON arranges resources/cameras and checks
state; it does not issue the player's trigger requests. Screenshots are native
captures, not image generation. These are not human unrestricted playthroughs,
natural-world long runs, latency certification or production capacity benchmarks.

## Multi-agent test scope

The progression soak uses 6000 accelerated game ticks per allocation count with
production runtime/scheduler logic and separately declared resource plots. No
online owner or per-action driver is supplied. Native tick-query output is
diagnostic evidence only: no natural-terrain or real-user latency claim follows.
