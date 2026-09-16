$data modify storage npcraft:uuid append.digit set from storage npcraft:uuid hex[$(index)]
data modify storage npcraft:uuid append.word set from storage npcraft:uuid word
function npcraft:identity/prepend with storage npcraft:uuid append
