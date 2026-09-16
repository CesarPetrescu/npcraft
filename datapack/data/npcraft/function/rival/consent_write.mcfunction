execute unless data storage npcraft:state consents run data modify storage npcraft:state consents set value []
$data remove storage npcraft:state consents[{id:$(id)}]
$data modify storage npcraft:state consents append value {id:$(id),token:$(token)}
