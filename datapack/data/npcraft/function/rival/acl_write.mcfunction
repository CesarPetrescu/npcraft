execute unless data storage npcraft:state acl run data modify storage npcraft:state acl set value []
$data remove storage npcraft:state acl[{id:$(id)}]
$data modify storage npcraft:state acl append value {id:$(id),allowed:$(allowed)b}
