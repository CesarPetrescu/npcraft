# Staged removal: caller must discard the whole snapshot on any insufficient input.
scoreboard players set #inv_ok np.tmp 0
$scoreboard players set #iv_need np.tmp $(count)
execute unless score #iv_need np.tmp matches 1..2304 run return 0
$function npcraft:inventory/remove_loop {slot:0,kind:"$(kind)"}
execute if score #iv_need np.tmp matches 0 run scoreboard players set #inv_ok np.tmp 1
