# Count only the current transaction snapshot. Result #iv_total.
scoreboard players set #iv_total np.tmp 0
$function npcraft:inventory/count_loop {slot:0,kind:"$(kind)"}
