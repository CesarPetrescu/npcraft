function npcraft:inventory/load
execute unless data entity @a[tag=npcraft.actor,limit=1] SelectedItem run return 0
scoreboard players set #iv_max_input np.tmp 0
execute if items entity @a[tag=npcraft.actor,limit=1] weapon.mainhand *[minecraft:max_stack_size=1] run scoreboard players set #iv_max_input np.tmp 1
execute if items entity @a[tag=npcraft.actor,limit=1] weapon.mainhand *[minecraft:max_stack_size=16] run scoreboard players set #iv_max_input np.tmp 16
execute if items entity @a[tag=npcraft.actor,limit=1] weapon.mainhand *[minecraft:max_stack_size=64] run scoreboard players set #iv_max_input np.tmp 64
execute if score #iv_max_input np.tmp matches 0 run return run tellraw @a[tag=npcraft.actor] {"text":"Only stack limits 1, 16 and 64 are supported.","color":"yellow"}
data modify storage npcraft:inv input.item set from entity @a[tag=npcraft.actor,limit=1] SelectedItem
execute store result storage npcraft:inv input.max int 1 run scoreboard players get #iv_max_input np.tmp
function npcraft:inventory/insert
execute unless score #inv_ok np.tmp matches 1 run return run tellraw @a[tag=npcraft.actor] {"text":"Backpack full; your held stack was not changed.","color":"yellow"}
execute store success score #iv_transferred np.tmp run item replace entity @a[tag=npcraft.actor,limit=1] weapon.mainhand with minecraft:air
execute if score #iv_transferred np.tmp matches 1 run function npcraft:inventory/commit
