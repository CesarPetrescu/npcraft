# Nonlethal starvation floor avoids silently deleting an unattended test companion.
execute if score #health np.tmp matches 2.. run function npcraft:survival/starve_damage with entity @s data
