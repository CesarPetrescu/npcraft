function npcraft:agent/init
tellraw @a[tag=npcraft.actor] [{"text":"Agent: ","color":"aqua"},{"nbt":"data.agent","entity":"@s"}]
tellraw @a[tag=npcraft.actor] [{"text":"36-slot backpack (hotbar is slots 0-8, not extra slots): ","color":"gray"},{"nbt":"data.inventory.slots","entity":"@s"}]
