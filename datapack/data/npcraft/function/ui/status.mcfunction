# Resolve snapshot values BEFORE sending the dialog. Client-side NBT components
# do not retain the marker executor context and otherwise render empty fields.
data modify storage npcraft:ui screen set value {type:"minecraft:notice",title:"NPCraft status",pause:false,body:[{type:"minecraft:plain_message",width:400,contents:[{text:"Goal: ",color:"aqua"},{text:"unassigned"}]},{type:"minecraft:plain_message",width:400,contents:[{text:"Now: "},{text:"idle"},{text:" | "},{text:"idle"}]},{type:"minecraft:plain_message",width:400,contents:[{text:"Reason: "},{text:"none"}]},{type:"minecraft:plain_message",width:400,contents:[{text:"Health: "},{text:"not enabled"},{text:" | Food: "},{text:"not enabled"}]},{type:"minecraft:plain_message",width:400,contents:[{text:"Rival activity: "},{text:"inactive"}]},{type:"minecraft:plain_message",width:400,contents:"Read-only snapshot. End rival with trigger npcraft set 42 from anywhere."}],action:{label:"Close"}}
execute if data entity @s data.agent.goal run data modify storage npcraft:ui screen.body[0].contents[1].text set from entity @s data.agent.goal
execute if data entity @s data.agent.intent run data modify storage npcraft:ui screen.body[1].contents[1].text set from entity @s data.agent.intent
execute if data entity @s data.agent.state run data modify storage npcraft:ui screen.body[1].contents[3].text set from entity @s data.agent.state
execute if data entity @s data.agent.reason run data modify storage npcraft:ui screen.body[2].contents[1].text set from entity @s data.agent.reason
execute if data entity @s data.survival{enabled:1b} if data entity @s data.survival.health if data entity @s data.survival.food run function npcraft:ui/status_vitals with entity @s data.survival
execute if data entity @s data.rival.activity run data modify storage npcraft:ui screen.body[4].contents[1].text set from entity @s data.rival.activity
function npcraft:ui/show with storage npcraft:ui
