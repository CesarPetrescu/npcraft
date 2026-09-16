# Original unsigned-word conversion. Input: uuid.parts = Minecraft UUID int array.
# Negative words are converted through their nonnegative bitwise complement, avoiding overflow.
data modify storage npcraft:uuid hex set value ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
data modify storage npcraft:uuid words set value []
scoreboard players set #hex_base np.tmp 16
function npcraft:identity/word {index:0}
function npcraft:identity/join
