# Operations and known failure boundaries

## Backups and upgrades

Use a separate test world. Back up the entire world before installation/upgrades,
not only datapacks: ownership and inventory live in entities, command storage and
scoreboards. Do not combine region files from one snapshot with scores/storage
from another and expect transaction consistency. Stop the server cleanly before
copying a production world.

Only schema 1 / Java 26.3 is implemented. Test an upgraded game separately; do not
merely edit pack.mcmeta to suppress compatibility warnings. A `/reload` retains
IDs, allocations, items and operator pause state. It clears only transient paths.

## Pausing and revocation

`npcraft:admin/pause` prevents new player mutations and autonomous work while leaving
records intact. The menu still opens. `npcraft:admin/revoke` run as a player removes
approval and pauses that owner's autonomous companions. Re-grant/resume restores
normal behavior. Normal work also requires the approved owner within 64 blocks.

## Stuck companions

Read Status. Unsupported floor shapes, trees outside the small plot, walls, altitude
changes, unloaded chunks and far-goal concave obstacles are expected safe stops.
Provide a flat full-block route, use Stay/Follow again, and remain nearby. The pack
does not mine a rescue tunnel or silently teleport the bot through a wall.

Status codes: 0 idle/arrived, 1 moved, 2 scanning, 3 cutting, 4 blocked, 5 barrel full,
6 missing axe, 7 missing plot, 8 missing barrel, 9 blocked line of sight. Some status
values persist until the next successful state update; they are diagnostics, not
a complete task timeline or a promise of autonomous error recovery.

## Items and permissions

Only the marker's `data.tool` and `data.cargo` are authoritative. Do not extract the
mannequin's displayed equipment using other plugins/admin commands. Ordinary users
should use Give/Return controls. Returned/dismissed items are physical world drops,
not private inventory transfers; nearby players can collect them.

This alpha intentionally uses invulnerable bodies. It does not implement generic
mob retaliation, survival hunger, equipment durability from combat, death drops,
respawn or inventory tombstones. Those are future work, not hidden features.

Allocation counts include unloaded controllers. Do not delete markers with `/kill`:
it destroys their authoritative items and leaves allocation metadata. Automatic
“missing entity” reclamation is unsafe because missing often just means unloaded.
Restore the backup after accidental manual deletion; do not reset counts while
unloaded companions may still exist. Missing cosmetic bodies are recreated when
an approved nearby owner allows that controller to run.

## Uninstall

Load each companion's area, select and dismiss it, and collect the dropped axe and
cargo. Check that every owner's count and the global count are zero, then remove
the ZIP/folder. The saved empty namespace data/objectives may remain; retaining
these is safer than deleting unrelated scores or losing unloaded records.

Do not call a global destructive cleanup routine on a live world; none is shipped.
Deleting the pack alone does not remove saved entities. For complete removal with
unknown/unloaded allocations, restoring the pre-install world backup is safest.
