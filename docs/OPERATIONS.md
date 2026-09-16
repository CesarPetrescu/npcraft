# Operating NPCraft 0.3

## Backups and upgrade

Back up the whole world while stopped: region/entities, scores, command storage,
player data and datapacks. Remove older NPCraft versions before installing this
one. Keep the exact tested Java version. Lazy additions preserve schema-1 IDs,
legacy timber tool/cargo and newer backpack records; do not delete old fields.
Never mix region files and command storage from inconsistent snapshots.

## Approval, pause, consent

Only approved owners issue ordinary companion commands. `admin/revoke` updates the
persistent ACL; `admin/pause` stops autonomous work/combat. Neither means existing
mortal bodies become immune to outside damage. Runtime death accounting may still
record and drop legitimate inventory while work is paused. Safe respawn waits
until the server is resumed. Action 42 revokes rival consent from anywhere, even
when paused, outside the Overworld or no longer approved. Use it before experimenting
with a new arena. Rival consent is separate from administrative permission.

Rivals work only in loaded chunks. No automatic force-loading/offline simulation.
A missing loaded body is treated conservatively as death for mortal controllers,
never an excuse to grant replacement equipment. Do not edit/delete controller NBT,
extract the displayed mannequin tool, or run blanket entity cleanup commands.

## Items, stations and death

Backpack and legacy timber inventory are authoritative; display equipment is not.
Returns and deaths create public drops, collectible by other players. The reserved
`minecraft:custom_data.npcraft_visual` flag is for disposable visual copies; do not
use it on user-generated real items. Death does not reclaim furnace contents or
remove stations. Check these blocks before uninstalling.

The corpse timer is primed while alive to avoid the targeted mannequin's invalid
DYING-pose serialization window. Tests check live health, actual damage, death and
restart. This is a compatibility workaround, not a claim of general player physics.

Food is supplied cooked beef/bread/apples, not autonomous farming. Respawn requires
safe loaded home cells and waits otherwise. Recovery seeks only real marked drops
for a limited time. Missing/stolen/despawned items are not reconstructed. Death or
world unloading can leave a furnace burning its remaining fuel normally.

## Blocked work

Use task/health view and work-bound preview. Every supported block inside the plot
is eligible, including player-placed construction. Provide clear full-block lanes,
reachable resources, spare coal and legal station space. Unsupported terrain,
replaced/foreign furnaces, full inventories and missing ingredients must stop safely.
It will not dig a rescue tunnel, silently teleport through walls, or bypass claims.

The no-gravity presentation is not certified knockback/fall/swim simulation. A safe
stop on natural terrain is expected when that terrain needs an unsupported action.

## Uninstall

Load each companion's area; end rival mode; dismiss it; collect returned items;
empty/reclaim stations. Confirm no remaining loaded or unloaded allocations before
removing the pack. Deleting the ZIP alone leaves saved entities. Restore a complete
pre-install backup if allocations are unknown. There is no global destructive
cleanup command: unloaded records cannot safely be assumed deleted.
