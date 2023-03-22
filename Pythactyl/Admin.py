import requests
from .objects import User, Node, NodeConfig, Allocation, Location, Server, HEADERS, Database, Nest, Egg
from .Errors import UserExists
class PterodactylAdmin(object):
    def __init__(self, url, api_key):
        self.url = url + "/api/application"
        self.api_key = api_key
        self.headers = HEADERS
        self.headers['Authorization'] = f"Bearer {self.api_key}"

    def listUsers(self):
        r = requests.get(self.url + "/users", headers=self.headers)
        users = []
        for item in r.json()['data']: # Get list of users
            users.append(User(item['attributes']))

        return users

    def getUser(self, userid: int):
        r = requests.get(self.url + "/users/" + str(userid), headers=self.headers)
        data = r.json()['attributes']
        user = User(data)
        return user

    def getByExternalID(self, exid):
        r = requests.get(self.url + "/users/external/" + str(exid), headers=self.headers)
        return r.json()

    def createUser(self, email, username, first, last, language="en", root_admin=False):
        data = {
            "email": email,
            "username": username,
            "first_name": first,
            "last_name": last,
            "language": language,
            "root_admin": root_admin
        }
        r = requests.post(self.url + "/users", headers=self.headers, json=data)

        if r.status_code == 422:
            raise UserExists("User already exists")

        data = r.json()['attributes']

        user = User(data)
        return user

    def editUser(self, userid, email, username, first_name, lastname, language, password, root_admin=None):
        data = {}
        data['email'] = email
        data['username'] = username
        data['first_name'] = first_name
        data['last_name'] = lastname
        data['language'] = language
        data['password'] = password
        data['root_admin'] = root_admin if root_admin else None

        r = requests.patch(self.url + "/users/" + str(userid), headers=self.headers, json=data)
        return User(r.json()['attributes'])

    def removeUser(self, userid):
        r = requests.delete(self.url + "/users/" + str(userid), headers=self.headers)
        return r.status_code == 204

    #   Nodes

    def listNodes(self):
        r = requests.get(self.url + "/nodes", headers=self.headers)
        nodes = []
        for data in r.json()['data']:
            node = Node(data['attributes'])
            nodes.append(node)
        return nodes

    def getNode(self, nodeid):
        r = requests.get(self.url + "/nodes/" + str(nodeid), headers=self.headers)
        return Node(r.json()['attributes'])

    def getNodeConfig(self, nodeid):
        r = requests.get(self.url + "/nodes/" + str(nodeid) + "/configuration", headers=self.headers)
        return NodeConfig(r.json())

    def createNode(self, name, location, fqdn, memory, disk,  scheme="https", memory_over=0, disk_over=0, upload_size=100, daemon_sftp=2022, daemon_listen=8080):
        data = {
            "name": name,
            "location_id": location,
            "fqdn": fqdn,
            "scheme": scheme,
            "memory": memory,
            "memory_overallocate": memory_over,
            "disk": disk,
            "disk_overallocate": disk_over,
            "upload_size": upload_size,
            "daemon_sftp": daemon_sftp,
            "daemon_listen": daemon_listen
        }
        r = requests.post(self.url + "/nodes", headers=self.headers, json=data)
        return Node(r.json()['attributes'])

    def updateNode(self, name=None, location=None, fqdn=None, scheme=None, memory=None, memory_over=None, disk=None, disk_over=None, upload_size=None, daemon_sftp=None, daemon_listen=None):
        data = {}
        if name:
            data['name'] = name
        if location:
            data['location_id'] = location
        if fqdn:
            data['fqdn'] = fqdn
        if scheme:
            data['scheme'] = scheme
        if memory:
            data['memory'] = memory
        if memory_over:
            data['memory_overallocate'] = memory_over
        if disk:
            data['disk'] = disk
        if upload_size:
            data['upload_size'] = upload_size
        if daemon_sftp:
            data['daemon_sftp'] = daemon_sftp
        if daemon_listen:
            data['daemon_listen'] = daemon_listen

        r = requests.put(self.url + "/nodes", headers=self.headers, json=data)
        return Node(r.json()['attributes'])

    def removeNode(self, nodeid):
        r = requests.delete(self.url + "/nodes/" + str(nodeid), headers=self.headers)
        return r.status_code == 204

    #   Allocations

    def listAllocations(self, nodeid):
        r = requests.get(self.url + "/nodes/" + str(nodeid) + "/allocations", headers=self.headers)
        allocations = []
        for allocation in r.json()['data']:
            allocations.append(Allocation(allocation['attributes']))

        return allocations

    def createAllocation(self, nodeid, ip, ports=[]):
        if len(ports) <= 0:
            raise SyntaxError("You must specify atleast 1 port")
        data = {
            "ip": ip,
            "ports": [str(a) for a in ports]
        }
        r = requests.post(self.url + "/nodes/" + str(nodeid) + "/allocations", headers=self.headers, json=data)
        return r.status_code == 204

    def removeAllocation(self, nodeid, allocationid):
        r = requests.delete(self.url + "/nodes/" + str(nodeid) + "/allocations/" + str(allocationid), headers=self.headers)
        return r.status_code == 204

    #   Locations

    def listLocations(self):
        r = requests.get(self.url + "/locations", headers=self.headers)
        locs = []
        for loc in r.json()['data']:
            locs.append(Location(loc['attributes']))
        return locs

    def getLocation(self, locationid):
        r = requests.get(self.url + "/locations/" + str(locationid), headers=self.headers)
        return Location(r.json()['attributes'])

    def createLocation(self, short, long):
        if len(short) > 4:
            raise TypeError("Your short location name must be less than 4 characters long")
        data = {
            "short": short,
            "long": long
        }
        r = requests.post(self.url + "/locations", headers=self.headers, json=data)
        return Location(r.json()['attributes'])

    def updateLocation(self, locationid, short=None, long=None):
        data = {}
        if short:
            if len(short) > 4:
                raise TypeError("Your short location name must be less than 4 characters long")
            data['short'] = short
        if long:
            data['long'] = long
        r = requests.put(self.url + "/locations/" + str(locationid), headers=self.headers, json=data)
        return Location(r.json()['attributes'])

    def removeLocation(self, locationid):
        r = requests.delete(self.url + "/locations/" + str(locationid), headers=self.headers)
        return r.status_code == 204

    #   Servers

    def listServers(self):
        r = requests.get(self.url + "/servers", headers=self.headers)
        _servers = []
        for serv in r.json()['data']:
            _servers.append(Server(serv['attributes']))
        return _servers

    def getServer(self, serverid):
        r = requests.get(self.url + "/servers/" + str(serverid), headers=self.headers)
        # setattr(self, "name", r[''])
        return Server(r.json()['attributes'])

    def getServerByExternalID(self, extid):
        r = requests.get(self.url + "/servers/external/" + str(extid), headers=self.headers)
        return r.json()

    def updateServer(self, serverid, name=None, user=None, externalid=None, description=None):
        data = {}
        if name:
            data['name'] = name
        if user:
            data['user'] = user
        if externalid:
            data['external_id'] = externalid
        if description:
            data['description'] = description

        r = requests.put(self.url + "/servers/" + str(serverid) + "/details", headers=self.headers, json=data)
        return Server(r.json()['attributes'])

    def updateServerBuild(self, serverid, allocation, memory=None, swap=None, io=None, cpu=None, disk=None, threads=None, feature_limits={'databases': 0, 'allocations': 3,'backups': 1}):
        data = {
            "allocation": allocation
        }
        if memory:
            data['memory'] = memory
        if swap:
            data['swap'] = swap
        if io:
            data['io'] = io
        if cpu:
            data['cpu'] = cpu
        if threads:
            data['threads'] = threads
        if feature_limits:
            data['feature_limits'] = feature_limits
        r = requests.put(self.url + "/servers/" + str(serverid) + "/build", headers=self.headers, json=data)
        return Server(r.json()['attributes'])

    def updateServerStartup(self, serverid, startup, egg, image, environment: dict=None, skip_scripts=False):
        data = {
            "startup": startup,
            "egg": egg,
            "image": image,
            "skip_scripts": skip_scripts
        }
        if environment:
            data['environment'] = environment

        r = requests.put(self.url + "/servers/" + str(serverid) + "/startup", headers=self.headers, json=data)
        return Server(r.json()['attributes'])

    def createServer(self, name, userid, eggid, image, startup, enviroment: dict, limits: dict, feature_limits: dict, allocation: dict):
        data = {
            'name': name,
            "user": userid,
            "egg": eggid,
            "docker_image": image,
            "startup": startup,
            "environment": enviroment,
            "limits": limits,
            "feature_limits": feature_limits,
            "allocation": allocation
        }
        r = requests.post(self.url + "/servers", headers=self.headers, json=data)
        if not r.status_code == 201:
            return r.json()
        return Server(r.json()['attributes'])

    def suspendServer(self, serverid):
        r = requests.post(self.url + "/servers/" + str(serverid) + "/suspend", headers=self.headers)
        return r.status_code == 204

    def unsuspendServer(self, serverid):
        r = requests.post(self.url + "/servers/" + str(serverid) + "/unsuspend", headers=self.headers)
        return r.status_code == 204

    def reinstallServer(self, serverid):
        r = requests.post(self.url + "/servers/" + str(serverid) + "/reinstall", headers=self.headers)
        return r.status_code == 204

    def deleteServer(self, serverid):
        r = requests.delete(self.url + "/servers/" + str(serverid), headers=self.headers)
        return r.status_code == 204

    def forceDeleteServer(self, serverid):
        r = requests.delete(self.url + "/servers/" + str(serverid) + "/force", headers=self.headers)
        return r.status_code == 204

    #   Server Databases

    def listServerDatabases(self, serverid, include_pass_host=False):
        r = requests.get(self.url + "/servers/" + str(serverid) + f"/databases{'?include=password,host' if include_pass_host else ''}", headers=self.headers)
        databases = []
        for db in r.json()['data']:
            databases.append(Database(db['attributes']))
        return databases

    def getServerDBDetails(self, serverid, db_id, include_pass_host=False):
        r = requests.get(self.url + "/servers/" + str(serverid) + f"/databases/" + str(db_id) + f"{'?include=password,host' if include_pass_host else ''}", headers=self.headers, json=data)
        return Database(r.json()['attributes'])

    def createServerDatabase(self, serverid ,db, remote="%", host=None):
        data = {
            "database": db,
            "remote": remote,
        }
        if host:
            data['host'] = host
        r = requests.post(self.url + "/servers/" + str(serverid) + "/databases", headers=self.headers, json=data)
        return Database(r.json()['attributes'])

    def resetServerDBPassword(self, serverid, dbid):
        r = requests.post(self.url + "/servers/" + str(serverid) + "/databases/" + str(db_id) + "/reset-password", headers=self.headers)
        return r.status_code == 204

    def removeServerDB(self, serverid, dbid):
        r = requests.delete(self.url + "/servers/" + str(serverid) + "/databases/" + str(db_id), headers=self.headers)
        return r.status_code == 204

    #   Nests

    def listNests(self, include_params=False):
        r = requests.get(self.url + f"/nests{'?include=eggs,servers' if include_params else ''}", headers=self.headers)
        nests = []
        for nest in r.json()['data']:
            nests.append(Nest(nest['attributes']))
        return nests

    def getNest(self, nestid, include_params=False):
        r = requests.get(self.url + f"/nests/{nestid}{'?include=eggs,servers' if include_params else ''}", headers=self.headers)
        return Nest(r.json()['attributes'])

    def listNestEggs(self, nestid, include_params=False):
        r = requests.get(self.url + f"/nests/{nestid}/eggs{'?include=nest,servers' if include_params else ''}", headers=self.headers)
        eggs = []
        for egg in r.json()['data']:
            eggs.append(Egg(egg['attributes']))
        return eggs

    def getNestEgg(self, nestid, eggid, include_params=True):
        r = requests.get(self.url + f"/nests/{nestid}/eggs/{eggid}{'?include=nest,servers,config,script,variables' if include_params else ''}", headers=self.headers)
        return Egg(r.json()['attributes'])
        # return r.json()


if __name__ == "__main__":
    print("I dont run. No use in trying to make me lol")
