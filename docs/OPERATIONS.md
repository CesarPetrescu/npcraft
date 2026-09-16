# Operations

## Backups and upgrades

Back up the **whole world**, including regions, entities, scoreboards and command
storage, with a clean shutdown. Do not mix different snapshots. Synchronous
inventory/action commits are not crash-proof database transactions across saves.
Use a separate test world before installation or an engine/datapack upgrade.

0.2 adds `data.inventory` and `data.agent` lazily to existing controllers. It does
not reset schema-1 owner UUIDs, IDs, legacy timber tools/cargo or allocation counters.
A `/reload` retains state and the operator pause flag. Do not downgrade once new
backpack items exist: an older pack cannot manage them. Do not merely change
pack.mcmeta to suppress compatibility warnings on another game version.

## Pausing and diagnosis

`npcraft:admin/pause` blocks mutations and work while retaining items/records.
`npcraft:admin/resume` re-enables it. Run `npcraft:admin/revoke` as a player to remove
approval. Autonomous work requires the approved owner within 64 blocks in the
Overworld. Missing/unloaded owners or controllers are paused, not reclaimed.

Use trigger 25 for the agent's intent, state, reason and backpack. Trigger 13 shows
legacy job diagnostics. Trigger 11 cancels. Status/panel reads do not cancel a cut;
unknown actions have no side effects. Trigger 22 stops work and returns backpack
contents as public drops. Other players can collect those drops.

For `assign_work_plot`/`assign_real_workbench`, set the missing target. For blocked
routes, provide a supported full-block approach with two clear body cells. One-block
up and at most two-block down transitions are supported; slabs/stair shapes, doors,
water and unsupported hazards can cause a safe stop. Temporary failed-target memory
expires; absent resources are not replaced with free items.

## Inventory ownership

The marker's backpack and legacy `data.tool`/`data.cargo` are authoritative. The
mannequin's displayed item is a cosmetic copy. Never extract it with another plugin
or administrative command and treat it as inventory. Bodies are deliberately
invulnerable; survival combat/death drops are not supported.

Do not blanket-kill controller markers: this destroys their items and leaves saved
allocation metadata. A missing controller may simply be unloaded, so automatic
reclamation is unsafe. Restore the full backup after accidental deletion.

Approved users are trusted to designate permitted work plots/containers/benches.
Vanilla commands do not automatically integrate arbitrary land-claim plugins.
Ordinary users cannot control another owner's NPC through the public trigger API;
operators can always tamper directly with scores/NBT and are outside that boundary.

## Uninstall

Load every companion's area, select and dismiss it, and collect all backpack plus
legacy tool/cargo drops. Confirm allocation counts are zero before removing the
pack. Merely deleting the ZIP leaves saved entities/state. Empty objectives/storage
may remain; retaining them is safer than deleting potentially unloaded records.
For unknown allocations, restoring the pre-install full-world backup is safest.
