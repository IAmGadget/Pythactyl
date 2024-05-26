import json

import requests

from Pythactyl.Errors import PermissionsMissing
from .objects import User, Node, NodeConfig, Allocation, Location, Server, Database, Nest, Egg, Key, \
    Relationship, ServerLimits, FeatureLimits, SFTP


class PterodactylClient(object):
    def __init__(self, url, api_key):
        if url.endswith("/"):
            url = url[:-1]
        self.url = url + "/api/client"
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        self.headers['Authorization'] = f"Bearer {self.api_key}"

    def __repr__(self):
        try:
            return f"<Pythactyl: {self.url} Account: {self.account().fname}>"
        except:
            return f"<Pythactyl: {self.url} Account: None>"

    #####################
    # ACCOUNT ENDPOINTS #
    #####################

    def account(self):
        r = requests.get(self.url + "/account", headers=self.headers).json()
        r = r['attributes']
        # return User(
        #     id=r['id'],
        #     email=r['email'],
        #     admin=r['admin'],
        #     fname=r['first_name'],
        #     lname=r['lname'],
        #     lang=r['language'],
        #     twofactor=self._check2fa()['data']  # This returns a QR code image
        # )
        return User(r)

    def check2fa(self):
        r = requests.get(self.url + "/account/two-factor", headers=self.headers).json()
        if r.get("data"):
            return True
        else:
            return False

    def updateEmail(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        r = requests.put(self.url + "/account/email", headers=self.headers, json=data)
        return r.status_code == 201

    def updatePassword(self, password, newpass, confpass):
        data = {
            "current_password": password,
            "password": newpass,
            "password_confirmation": confpass
        }
        r = requests.put(self.url + "/account/email", headers=self.headers, json=data)
        return r.status_code == 204
    ############
    # API KEYS #
    ############
    def listApikeys(self):
        r = requests.get(self.url + "/account/api-keys", headers=self.headers).json()
        return [].append([x for x in r['data']])

    def createApiKey(self, description, allowed_ips=[]):
        data = {
            "description": description,
            "allowed_ips": allowed_ips
        }
        r = requests.post(self.url + "/account/api-keys", headers=self.headers, json=data).json()
        meta = r['meta']
        r = r['attributes']
        return Key(
            identifer=r['identifier'],
            description=r['description'],
            allowed_ips=r['allowed_ips'],
            lastused=r['last_used_at'],
            created_at=r['created_at'],
            token=meta['secret_token']
        )

    def removeApiKey(self, code):
        r = requests.delete(self.url + "/account/api-keys/" + str(code), headers=self.headers)
        if r.status_code == 404:
            return {'error': 'An error has occured','tips': 'Check the code is correct and/or existing'}
        else:
            return r.status_code == 204

    ###########
    # Servers #
    ###########
    def listServers(self):
        r = requests.get(self.url, headers=self.headers).json()
        _servers = []
        for server in r['data']:
            _relationships = []
            if server.get('relationships'):
                for x in server['relationships']['allocations']['data']:
                    _relationships.append(
                        Relationship(x['attributes']['id'], x['attributes']['ip'], x['attributes']['ip_alias'],
                                             x['attributes']['port'], x['attributes'], x['attributes']['notes'],
                                             x['attributes']['is_default']))

            # _servers.append(Server(server))
            server = server['attributes']
            _servers.append(Server(server))
        return _servers

    def getServer(self, identifier):
        r = requests.get(self.url + "/servers/" + str(identifier), headers=self.headers).json()
        return Server(r['attributes'])

    def sendPowerAction(self, identifier, action):
        signals = ['start', 'stop','restart','kill']
        if action.lower() not in signals:
            return {'error': 'Incorrect signal sent','available signals': signals}
        data = {
            "signal": action
        }
        r = requests.post(self.url + "/servers/" + identifier + "/power", headers=self.headers, json=data)
        return r.status_code == 204

    def sendCommand(self, identifier, command):
        data = {
            "command": command
        }
        r = requests.post(self.url + "/servers/" + identifier + "/command", headers=self.headers, json=data)
        return r.status_code == 204

    def listDatabases(self, identifier):
        r = requests.get(self.url + "/servers/" + str(identifier) + "/databases", headers=self.headers).json()
        if r.get('data') is None:
            return []
        dbs = []
        for db in r['data']:
            print(db)
            dbs.append(Database(db['attributes']))
        return dbs

    def createDatabase(self, identifier, db_name, remote_addr="%"):
        data = {
            "database": db_name,
            "remote": remote_addr
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/databases", headers=self.headers, json=data)
        return Database(r.json()['attributes'])

    def rotateDatabasePassword(self, identifier, db_id):
        r = requests.post(self.url + "/servers/" + str(identifier) + "/databases/" + db_id + "/rotate-password", headers=self.headers)
        return Database(r.json()['attributes'])

    def removeDatabase(self, identifier, db_id):
        r = requests.delete(self.url + "/servers/" + str(identifier) + "/databases/" + db_id + "rotate-password", headers=self.headers)
        return r.json()

    #   Subusers

    def listSubusers(self, identifier):
        r = requests.get(self.url + "/servers/" + str(identifier) + "/users", headers=self.headers)
        return r.json()

    def addSubuser(self, identifier, email, permissions=[]):

        if len(permissions) <= 0:
            raise PermissionsMissing("You must specify at least 1 permission node")
        data = {
            "email": email,
            "permissions": permissions
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/users", headers=self.headers, json=data)
        return r.json()

    def getSubuser(self, identifier, uuid):
        r = requests.get(self.url + "/servers/" + str(identifier) + "/users/" + uuid, headers=self.headers)
        return r.json()

    def updateSubuser(self, identifier, uuid, permissions=[]):
        if len(permissions) <= 0:
            raise PermissionsMissing("You must specify at least 1 permission node")
        data = {
            "permissions": permissions
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/users/" + uuid, headers=self.headers, json=data)
        return r.json()

    def removeSubuser(self, identifier, uuid):
        r = requests.delete(self.url + "/servers/" + str(identifier) + "/users/" + uuid, headers=self.headers, json=data)
        return r.json()

if __name__ == "__main__":
    print("I dont run. No use in trying to make me lol")
