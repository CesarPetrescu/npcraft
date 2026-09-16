execute unless data entity @s data.plot run return run tellraw @a[tag=npcraft.actor] {text:"Assign a work plot first.",color:"yellow"}
function npcraft:ui/plot_at with entity @s data.plot
tellraw @a[tag=npcraft.actor] {text:"Outline: 7 x 7 x 4 permitted work volume. All supported blocks inside are eligible, including player builds.",color:"yellow"}
