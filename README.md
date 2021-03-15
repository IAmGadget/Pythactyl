# Pythactyl
This python API wrapper is one of my first largest API wrapper's I have ever done. I do expect there to be bugs. Feel free to contribute

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


## information
I will be uploading documentation when the wrapper is completed. If you wish to know more syntax, you'll either have to source code dive or DM me: Gadget#0975.

## Contributors
IAmGadget
