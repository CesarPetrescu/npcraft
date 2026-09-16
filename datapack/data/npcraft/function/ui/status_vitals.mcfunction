# Only server-written numeric health/food values are interpolated into text.
$data modify storage npcraft:ui screen.body[3].contents[1].text set value "$(health)"
$data modify storage npcraft:ui screen.body[3].contents[3].text set value "$(food)"
