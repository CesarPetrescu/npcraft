$scoreboard players set @s np.id $(id)
tag @s add npcraft.body
# Invulnerable cosmetic body: real cargo/tool ownership stays on the marker controller.
$data merge entity @s {Invulnerable:1b,NoGravity:1b,Silent:1b,immovable:1b,hide_description:1b,CustomName:{text:"NPCraft #$(id)",color:"aqua"},CustomNameVisible:1b}
