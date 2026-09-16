data modify storage npcraft:uuid join.a set from storage npcraft:uuid words[0]
data modify storage npcraft:uuid join.b set from storage npcraft:uuid words[1]
data modify storage npcraft:uuid join.c set from storage npcraft:uuid words[2]
data modify storage npcraft:uuid join.d set from storage npcraft:uuid words[3]
function npcraft:identity/flat with storage npcraft:uuid join
data modify storage npcraft:uuid final.a set string storage npcraft:uuid flat 0 8
data modify storage npcraft:uuid final.b set string storage npcraft:uuid flat 8 12
data modify storage npcraft:uuid final.c set string storage npcraft:uuid flat 12 16
data modify storage npcraft:uuid final.d set string storage npcraft:uuid flat 16 20
data modify storage npcraft:uuid final.e set string storage npcraft:uuid flat 20 32
function npcraft:identity/format with storage npcraft:uuid final
