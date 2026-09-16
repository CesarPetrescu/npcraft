# Consent withdrawal must work remotely, in any dimension, without approval or a selected NPC.
execute store result storage npcraft:scratch consent.id int 1 run scoreboard players get @s np.owner
function npcraft:rival/revoke_consent with storage npcraft:scratch consent
tellraw @s {text:"All your rival consent is revoked, including unloaded rivals.",color:"green"}
