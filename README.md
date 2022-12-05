# Pythactyl
This Pterodactyl panel API wrapper is an unofficial wrapper. I made this in my free time and intend to improve as I go along 

## Install

    python -m pip install git+https://github.com/IAmGadget/Pythactyl

## Client

    from Pythactyl import Client

    client = client.PterodactylClient('URL', 'API KEY')

    client.account() # Retrieves the current account's information

    client.updateEmail('currentPassword', 'NewPassword', 'NewPassword')

    client.listServers() # This will return a JSON object of all the servers the client currently owns. (This is not including admin servers.)

    # Send a simple power action to your server

    server = client.getServer('identifier')['attributes']['identifier']

    cliend.sendPowerAction(server, "start")

## Admin

    from Pythactyl import admin

    admin = admin.PterodactylClient('URL', 'API KEY')

    user = admin.createUser('email@email.com', 'Bob', 'Simmons', root_admin=True)

    admin.editUser(user['id'], username="INeedANewName")


## Information
I will be uploading documentation when the wrapper is completed. If you wish to know more syntax, you'll either have to source code dive or DM me: Gadget#0975.

## Need help?
Join my discord for more support on this wrapper: https://discord.gg/SBXBd8sC5f