# Pythactyl
This Pterodactyl panel API wrapper is an unofficial wrapper. I made this in my free time and intend to improve as I go along 

## Install

    python -m pip install pythactyl

## Client

    from Pythactyl.Client import PterodactylClient
    
    client = PterodactylClient(url="https://panel.address.com", api_key="clientAPI")
    
    personal = client.listServers()
    
    print([x for x.name in personal])

    >> ['Fivem Server', 'Minecraft server awesome', 'Teamspeak 1.22']

## Admin

    from Pythactyl.Admin import PterodactylAdmin

    admin = PterodactylAdmin(url="https://panel.address.com", api_key="adminAPI"))

    user = admin.createUser('email@email.com', 'Bob', 'Simmons', root_admin=True)

    admin.editUser(user.id, username="INeedANewName")


## Information
I will be uploading documentation when the wrapper is completed. If you wish to know more syntax, you'll either have to source code dive or DM me: Gadget#6181.

## Need help?
Join my discord for more support on this wrapper: https://discord.gg/gnpZRcYqcn