scoreboard players set @s np.status 4
scoreboard players operation @s np.next = #now np.sys
scoreboard players add @s np.next 20
data remove entity @s data.navigation
return 0
