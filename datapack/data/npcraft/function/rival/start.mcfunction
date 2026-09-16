# Only the authorizing player becomes an opponent; other players are never damage targets.
execute unless entity @a[tag=npcraft.actor,gamemode=!creative,gamemode=!spectator,limit=1] run return run tellraw @a[tag=npcraft.actor] {text:"Switch to Survival or Adventure, then confirm the duel.",color:"yellow"}
execute unless data entity @s data.plot run return run tellraw @a[tag=npcraft.actor] {text:"Assign a permitted resource plot first.",color:"yellow"}
execute as @a[tag=npcraft.actor,limit=1] run function npcraft:rival/acl_grant
function npcraft:survival/enable
data modify entity @s data.rival set value {version:1,enabled:1b,retreat:0b,attack_at:0,react_at:0,seen_at:-1000,activity:"equipping"}
scoreboard players add #duel np.sys 1
execute store result entity @s data.rival.token int 1 run scoreboard players get #duel np.sys
data modify storage npcraft:scratch consent.id set from entity @s data.owner
execute store result storage npcraft:scratch consent.token int 1 run scoreboard players get #duel np.sys
function npcraft:rival/consent_write with storage npcraft:scratch consent
data modify entity @s data.rival.opponent set from entity @a[tag=npcraft.actor,limit=1] UUID
data modify entity @s data.rival.center set from entity @s data.home
data modify entity @s data.agent.goal set value "rival_kit"
data remove entity @s data.navigation
scoreboard players set @s np.mode 6
scoreboard players set @s np.next 0
tellraw @a[tag=npcraft.actor] {text:"Rival enabled: native damage/death, bounded arena, and only YOU are its opponent. Use trigger npcraft set 42 to end.",color:"red"}
