# Revalidate the actual next cell; searches never grant block-breaking permission.
data modify storage npcraft:nav step set value {}
data modify storage npcraft:nav step.x set from storage npcraft:nav first[0]
data modify storage npcraft:nav step.y set from storage npcraft:nav first[1]
data modify storage npcraft:nav step.z set from storage npcraft:nav first[2]
function npcraft:nav/move_macro with storage npcraft:nav step
