$execute unless data storage npcraft:state acl[{id:$(owner),allowed:1b}] run return 0
data modify storage npcraft:scratch consent.id set from entity @s data.owner
data modify storage npcraft:scratch consent.token set from entity @s data.rival.token
function npcraft:rival/consent_check with storage npcraft:scratch consent
