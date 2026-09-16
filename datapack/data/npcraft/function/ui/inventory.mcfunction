function npcraft:agent/init
data modify storage npcraft:ui screen set value {type:"minecraft:notice",title:"NPCraft backpack",pause:false,body:[{type:"minecraft:plain_message",width:420,contents:"36 total slots. This view is read-only. Give/return controls preserve full item data; returns are public drops."}],action:{label:"Close"}}
function npcraft:ui/slot {slot:0}
function npcraft:ui/show with storage npcraft:ui
