# Pythactyl
This Pterodactyl panel API wrapper is an unofficial wrapper. I made this in my free time and intend to improve as I go along 

## Install
    python -m pip install git+https://github.com/IAmGadget/Pythactyl
---
## Client

    from Pythactyl.Client import PterodactylClient
    
    client = PterodactylClient(url="https://panel.address.com", api_key="clientAPI")
    
    personal = client.listServers()
    
    print([x for x.name in personal])

    >> ['Fivem Server', 'Minecraft server awesome', 'Teamspeak 1.22']
---
## Admin

    from Pythactyl.Admin import PterodactylAdmin

    admin = PterodactylAdmin(url="https://panel.address.com", api_key="adminAPI"))

    user = admin.createUser('email@email.com', 'Bob', 'Simmons', root_admin=True)

    admin.editUser(user.id, username="INeedANewName")

---
## FAQ
### Where do I find the Client API key?
https://panel.com/account/api
### Where do I find the Admin API key?
https://panel.com/admin/api
### Are there any examples?
I have provided some examples in [Examples](https://github.com/IAmGadget/Pythactyl/tree/master/Pythactyl/examples)
### Will there be any documentation?
I am working on the documentation as I improve the API wrapper. For now all that I have provided in the above code should get you going. If you use an IDE such as Pycharm it will offer all the options given for both **Client** and **Admin** classes

---
## Need help?
Join my discord for more support on this wrapper: [Official discord support for Pythactyl](https://discord.gg/yAwYt4FD6E)
