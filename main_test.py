from Pythactyl.Admin import PterodactylAdmin
from Pythactyl.Client import PterodactylClient


admin = PterodactylAdmin("https://panel.jgamingz.dev", "ptla_46QJqIbvn9Rr597ujPyy2ffPoVFBACsyCzG750GYRwz")

client = PterodactylClient("https://panel.jgamingz.dev", "ptlc_MFUZN3lTMcbxXalKs8Jcez2RJiSHBviZPKWsFAn1GNe")

# client.listServers()
x = admin.listUsers()
print([a.username for a in x])