$data modify storage npcraft:inv compare set from storage npcraft:inv slots[$(slot)].item
scoreboard players set #pick_damage np.tmp 0
execute store result score #pick_damage np.tmp run data get storage npcraft:inv compare.components."minecraft:damage"
$scoreboard players set #pick_limit np.tmp $(durability)
execute if score #pick_damage np.tmp >= #pick_limit np.tmp run return 0
execute unless score #pick_damage np.tmp matches 0.. run return 0
data remove storage npcraft:inv compare.components."minecraft:damage"
execute unless data storage npcraft:inv compare.components run data modify storage npcraft:inv compare.components set value {}
$execute store success score #pick_different np.tmp run data modify storage npcraft:inv compare set value {id:"$(kind)",count:1,components:{}}
execute unless score #pick_different np.tmp matches 0 run return 0
# Prefer the stronger supported tier, never arbitrary inventory iteration order.
execute unless score #pick_limit np.tmp > #pick_best np.tmp run return 0
scoreboard players operation #pick_best np.tmp = #pick_limit np.tmp
$scoreboard players set #pick_slot np.tmp $(slot)
$data modify storage npcraft:inv pick set value {slot:$(slot),durability:$(durability)}
