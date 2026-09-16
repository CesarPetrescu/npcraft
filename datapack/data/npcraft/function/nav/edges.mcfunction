# Each candidate is one horizontal cell, with at most one block of elevation change.
function npcraft:nav/neighbor
execute if score #up_clear np.tmp matches 1 if block ~ ~ ~ #npcraft:floor positioned ~ ~1 ~ run function npcraft:nav/neighbor
execute if block ~ ~1 ~ #npcraft:clear positioned ~ ~-1 ~ run function npcraft:nav/neighbor
