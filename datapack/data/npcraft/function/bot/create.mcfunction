tag @s add npcraft.bot
scoreboard players operation @s np.id = #next np.sys
scoreboard players operation @s np.owner = #actor np.tmp
scoreboard players set @s np.mode 0
scoreboard players set @s np.status 0
scoreboard players set @s np.next 0
scoreboard players set @s np.dig 0
scoreboard players set @s np.harvest 0
data modify entity @s data set value {schema:1,scan:0,scanned:0,home:{},dest:{}}
execute store result entity @s data.id int 1 run scoreboard players get @s np.id
execute store result entity @s data.owner int 1 run scoreboard players get @s np.owner
data modify entity @s data.owner_uuid set from entity @a[tag=npcraft.actor,limit=1] UUID
execute store result entity @s data.home.x int 1 run data get entity @s Pos[0]
execute store result entity @s data.home.y int 1 run data get entity @s Pos[1]
execute store result entity @s data.home.z int 1 run data get entity @s Pos[2]
data modify storage npcraft:scratch entry set value {}
data modify storage npcraft:scratch entry.id set from entity @s data.id
data modify storage npcraft:state queue append from storage npcraft:scratch entry
function npcraft:bot/sync with entity @s data
