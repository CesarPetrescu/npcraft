$execute unless block $(x) $(y) $(z) minecraft:barrel run return run scoreboard players set @s np.status 8
execute store result score #by np.tmp run data get entity @s Pos[1]
$scoreboard players set #sy np.tmp $(y)
scoreboard players operation #sy np.tmp -= #by np.tmp
execute unless score #sy np.tmp matches -1..1 run return run scoreboard players set @s np.status 4
scoreboard players set #slot np.tmp -1
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.0 * run scoreboard players set #slot np.tmp 0
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.1 * run scoreboard players set #slot np.tmp 1
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.2 * run scoreboard players set #slot np.tmp 2
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.3 * run scoreboard players set #slot np.tmp 3
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.4 * run scoreboard players set #slot np.tmp 4
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.5 * run scoreboard players set #slot np.tmp 5
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.6 * run scoreboard players set #slot np.tmp 6
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.7 * run scoreboard players set #slot np.tmp 7
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.8 * run scoreboard players set #slot np.tmp 8
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.9 * run scoreboard players set #slot np.tmp 9
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.10 * run scoreboard players set #slot np.tmp 10
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.11 * run scoreboard players set #slot np.tmp 11
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.12 * run scoreboard players set #slot np.tmp 12
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.13 * run scoreboard players set #slot np.tmp 13
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.14 * run scoreboard players set #slot np.tmp 14
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.15 * run scoreboard players set #slot np.tmp 15
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.16 * run scoreboard players set #slot np.tmp 16
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.17 * run scoreboard players set #slot np.tmp 17
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.18 * run scoreboard players set #slot np.tmp 18
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.19 * run scoreboard players set #slot np.tmp 19
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.20 * run scoreboard players set #slot np.tmp 20
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.21 * run scoreboard players set #slot np.tmp 21
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.22 * run scoreboard players set #slot np.tmp 22
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.23 * run scoreboard players set #slot np.tmp 23
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.24 * run scoreboard players set #slot np.tmp 24
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.25 * run scoreboard players set #slot np.tmp 25
$execute if score #slot np.tmp matches -1 unless items block $(x) $(y) $(z) container.26 * run scoreboard players set #slot np.tmp 26
execute if score #slot np.tmp matches -1 run return run scoreboard players set @s np.status 5
data modify storage npcraft:scratch transfer set from entity @s data.storage
execute store result storage npcraft:scratch transfer.slot int 1 run scoreboard players get #slot np.tmp
data modify storage npcraft:scratch transfer.kind set from entity @s data.cargo.id
data modify storage npcraft:scratch transfer.count set from entity @s data.cargo.count
function npcraft:work/transfer with storage npcraft:scratch transfer
