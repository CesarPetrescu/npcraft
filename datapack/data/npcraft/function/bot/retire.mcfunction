# Clear presentation copies and expire on the next vanilla living-entity tick.
# Avoid /kill's unsupported DYING mannequin pose being serialized during a save.
item replace entity @s weapon.mainhand with minecraft:air
tag @s remove npcraft.body
tag @s add npcraft.retiring
data merge entity @s {Health:0.0f,DeathTime:19s,pose:"standing"}
