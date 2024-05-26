import requests
from .objects import User, Node, NodeConfig, Allocation, Location, Server, HEADERS, Database, Nest, Egg, Key, \
    Relationship, ServerLimits, FeatureLimits, SFTP


class PterodactylClient(object):
    def __init__(self, url, api_key):
        self.url = url + "/api/client"
        self.api_key = api_key
        self.headers = HEADERS
        self.headers['Authorization'] = f"Bearer {self.api_key}"

    def account(self):
        r = requests.get(self.url + "/account", headers=self.headers).json()
        r = r['attributes']
        return User(
            id=r['id'],
            email=r['email'],
            admin=r['admin'],
            fname=r['first_name'],
            lname=r['lname'],
            lang=r['language'],
            twofactor=self._check2fa()['data']  # This returns a QR code image
        )

    def _check2fa(self):
        r = requests.get(self.url + "/account/two-factor", headers=self.headers)
        return r.json()

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
    #       Servers
    def listServers(self):
        r = requests.get(self.url, headers=self.headers).json()
        _servers = []
        for server in r['data']:
            _relationships = []
            for x in server['relationships']['allocations']['data']:
                _relationships.append(
                    Relationship(x['attributes']['id'], x['attributes']['ip'], x['attributes']['ip_alias'],
                                         x['attributes']['port'], x['attributes'], x['attributes']['notes'],
                                         x['attributes']['is_default']))
            _servers.append(Server(
                owner=server['owner'],
                identifier=server['identifier'],
                uuid=server['uuid'],
                name=server['name'],
                node=server['node'],
                sftp=SFTP(server['sftp_details']['ip'], server['sftp_details']['port']),
                description=server['description'],
                limits=ServerLimits(server['limits']['memory'], server['limits']['swap'], server['limits']['disk'], server['limits']['io'], server['limits']['cpu']),
                feature_limits=FeatureLimits(server['feature_limits']['databases'], server['feature_limits']['allocations'], server['feature_limits']['backups']),
                suspended=server['is_suspended'],
                installing=server['is_installing'],
                relationships=_relationships
            ))
        return _servers

    def getServer(self, identifier):
        r = requests.get(self.url + "/servers/" + str(identifier), headers=self.headers)
        return r.json()

    def sendPowerAction(self, identifier, action):
        signals = ['start', 'stop','restart','kill']
        if action.lower() not in signals:
            return {'error': 'Incorrect signal sent','available signals': signals}
        data = {
            "signal": action
        }
        r = requests.post(self.url + "/servers/" + identifier + "/power", headers=self.headers, json=data)
        return r

    def sendCommand(self, identifier, command):
        data = {
            "command": command
        }
        r = requests.post(self.url + "/servers/" + identifier + "/command", headers=self.headers, json=data)
        return r

    def listDatabases(self, identifier):
        r = requests.get(self.url + "/servers/" + str(identifier) + "/databases", headers=self.headers)
        return r.json()

    def createDatabase(self, identifier, db_name, remote_addr="%"):
        data = {
            "database": db_name,
            "remote": remote_addr
        }
        r = requests.post(self.url + "/servers/" + str(identifier) + "/databases", headers=self.headers, json=data)
        return r.json()

    def resetDatabasePassword(self, identifier, db_id):
        r = requests.post(self.url + "/servers/" + str(identifier) + "/databases/" + db_id + "/rotate-password", headers=self.headers)
        return r.json()

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
