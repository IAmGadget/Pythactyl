import requests

class PterodactylClient(object):
    def __init__(self, url, api_key):
        self.url = url + "/api/client"
        self.api_key = api_key

    def account(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/account", headers=headers)
        return r.json()

    def check2fa(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/account/two-factor", headers=headers)
        return r.json()

    def updateEmail(self, email, password):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "email": email,
            "password": password
        }
        r = requests.put(self.url + "/account/email", headers=headers, json=data)
        return r.status_code

    def updatePassword(self, password, newpass, confpass):
        if newpass != confpass:
            return PasswordsDontMatch(f"{newpass} does not match {confpass}. Check spelling")
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "current_password": password,
            "password": newpass,
            "password_confirmation": confpass
        }
        r = requests.put(self.url + "/account/email", headers=headers, json=data)
        return r.json()

    def listApikeys(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/account/api-keys", headers=headers)
        return r.json()

    def createApiKey(self, description, allowed_ips=[]):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "description": description,
            "allowed_ips": allowed_ips
        }
        r = requests.post(self.url + "/account/api-keys", headers=headers, json=data)
        return r.json()

    def removeApiKey(self, code):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/account/api-keys/" + str(code), headers=headers)
        if r.status_code == 404:
            return {'error': 'An error has occured','tips': 'Check the code is correct and/or existing'}
        else:
            return r.status_code

    #       Servers
    def listServers(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url, headers=headers)
        return r.json()

    def getServer(self, identifier):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(identifier), headers=headers)
        return r.json()

    def sendPowerAction(self, identifier, action):
        signals = ['start', 'stop','restart','kill']
        if action.lower() not in signals:
            return {'error': 'Incorrect signal sent','available signals': signal}
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "signal": action
        }
        r = requests.post(self.url + "/servers/" + identifier + "/power", headers=headers, json=data)
        return r

    def sendCommand(self, identifier, command):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "command": command
        }
        r = requests.post(self.url + "/servers/" + identifier + "/command", headers=headers, json=data)
        return r

    def listDatabases(self, identifier):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(identifier) + "/databases", headers=headers)
        return r.json()

    def createDatabase(self, identifier, db_name, remote_addr="%"):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "database": db_name,
            "remote": remote_addr
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/databases", headers=headers, json=data)
        return r.json()

    def resetDatabasePassword(self, identifier, db_id):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/databases/" + db_id + "/rotate-password", headers=headers)
        return r.json()

    def removeDatabase(self, identifier, db_id):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/servers/" + str(identifier) + "/databases/" + db_id + "rotate-password", headers=headers)
        return r.json()

    #   Subusers

    def listSubusers(self, identifier):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(identifier) + "/users", headers=headers)
        return r.json()

    def addSubuser(self, identifier, email, permissions=[]):
        if len(permissions) <= 0:
            raise PermissionsMissing("You must specify at least 1 permission node")
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "email": email,
            "permissions": permissions
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/users", headers=headers, json=data)
        return r.json()

    def getSubuser(self, identifier, uuid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(identifier) + "/users/" + uuid, headers=headers)
        return r.json()

    def updateSubuser(self, identifier, uuid, permissions=[]):
        if len(permissions) <= 0:
            raise PermissionsMissing("You must specify at least 1 permission node")
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "permissions": permissions
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/users/" + uuid, headers=headers, json=data)
        return r.json()

    def removeSubuser(self, identifier, uuid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/servers/" + str(identifier) + "/users/" + uuid, headers=headers, json=data)
        return r.json()

if __name__ == "__main__":
    print("I dont run. No use in trying to make me lol")
