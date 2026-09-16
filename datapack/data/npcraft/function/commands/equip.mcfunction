execute if data entity @s data.tool run return run tellraw @a[tag=npcraft.actor] {"text":"Return the current axe first.","color":"yellow"}
execute unless items entity @a[tag=npcraft.actor,limit=1] weapon.mainhand minecraft:iron_axe[minecraft:enchantments={},!minecraft:unbreakable,minecraft:max_damage=250,minecraft:max_stack_size=1] run return run tellraw @a[tag=npcraft.actor] {"text":"Hold an unenchanted, breakable iron axe with standard durability. Damaged/named axes are accepted.","color":"yellow"}
data modify entity @s data.tool set from entity @a[tag=npcraft.actor,limit=1] SelectedItem
execute store success score #transferred np.tmp run item replace entity @a[tag=npcraft.actor,limit=1] weapon.mainhand with minecraft:air
execute unless score #transferred np.tmp matches 1 run data remove entity @s data.tool
function npcraft:bot/sync with entity @s data
