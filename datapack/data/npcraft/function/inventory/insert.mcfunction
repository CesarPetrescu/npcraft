# Input: inv.slots (snapshot), inv.input={item:<full stack>,max:1|16|64}.
# Output: #inv_ok; staged slots only. Never writes authoritative inventory itself.
scoreboard players set #inv_ok np.tmp 0
scoreboard players set #iv_left np.tmp 0
execute unless data storage npcraft:inv input.item.id run return 0
execute store result score #iv_left np.tmp run data get storage npcraft:inv input.item.count
execute store result score #iv_max np.tmp run data get storage npcraft:inv input.max
execute unless score #iv_left np.tmp matches 1..64 run return 0
execute unless score #iv_max np.tmp matches 1 unless score #iv_max np.tmp matches 16 unless score #iv_max np.tmp matches 64 run return 0
execute if score #iv_left np.tmp > #iv_max np.tmp run return 0
data modify storage npcraft:inv key set from storage npcraft:inv input.item
data modify storage npcraft:inv key.count set value 1
function npcraft:inventory/merge {slot:0}
function npcraft:inventory/empty {slot:0}
execute if score #iv_left np.tmp matches 0 run scoreboard players set #inv_ok np.tmp 1
