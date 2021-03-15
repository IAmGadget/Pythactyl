import requests
from errors import NotEnoughArugments, MissingData

class PterodactylClient(object):
    def __init__(self, url, api_key):
        self.url = url + "/api/application"
        self.api_key = api_key

    def listUsers(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/users", headers=headers)
        return r.json()

    def getUser(self, userid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/users/" + str(userid), headers=headers)
        return r.json()

    def getByExternalID(self, exid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/users/external/" + str(exid), headers=headers)
        return r.json()

    def createUser(self, email, username, first, last, language="en", root_admin=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "email": email,
            "username": username,
            "first_name": first,
            "last_name": last,
            "language": language,
            "root_admin": root_admin
        }
        r = requests.post(self.url + "/users", headers=headers, json=data)
        return r.json()

    def editUser(self, userid, email=None, username=None, first_name=None, language=None, password=None, root_admin=None):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {}
        if email:
            data['email'] = email
        if username:
            data['username'] = username
        if first_name:
            data['first_name'] = first_name
        if language:
            data['language'] = language
        if password:
            data['password'] = password
        if root_admin:
            data['root_admin'] = root_admin

        r = requests.patch(self.url + "/users/" + str(userid), headers=headers, json=data)
        return r.json()

    def removeUser(selfm, userid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/users/" + str(userid), headers=headers)
        return r.json()

    #   Nodes

    def listNodes(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/nodes", headers=headers)
        return r.json()

    def getNode(self, nodeid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/nodes/" + str(nodeid), headers=headers)
        return r.json()

    def getNodeConfig(self, nodeid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/nodes/" + str(nodeid) + "/configuration", headers=headers)
        return r.json()

    def createNode(self, name, location, fqdn, memory, disk,  scheme="https", memory_over=0, disk_over=0, upload_size=100, daemon_sftp=2022, daemon_listen=8080):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
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
        r = requests.post(self.url + "/nodes", headers=headers, json=data)
        return r.json()

    def updateNode(self, name=None, location=None, fqdn=None, scheme=None, memory=None, memory_over=None, disk=None, disk_over=None, upload_size=None, daemon_sftp=None, daemon_listen=None):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
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

        r = requests.put(self.url + "/nodes", headers=headers, json=data)
        return r.json()

    def removeNode(self, nodeid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/nodes/" + str(nodeid), headers=headers, json=data)
        return r.json()

    #   Allocations

    def listAllocations(self, nodeid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/nodes/" + str(nodeid) + "/allocations", headers=headers)
        return r.json()

    def createAllocation(self, nodeid, ip, ports=[]):
        if len(ports) <= 0:
            raise NotEnoughArugments("You must specify atleast 1 port")
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "ip": ip,
            "ports": ports
        }
        r = requests.post(self.url + "/nodes", headers=headers, json=data)
        return r.json()

    def removeAllocation(self, nodeid, allocationid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/nodes/" + str(nodeid) + "/allocations/" + allocationid, headers=headers, json=data)
        return r.json()

    #   Locations

    def listLocations(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/locations", headers=headers)
        return r.json()

    def getLocation(self, locationid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/locations/" + str(locationid), headers=headers)
        return r.json()

    def createLocation(self, short, long):
        if len(short) > 4:
            raise LocationShortTooLong("Your short location name is much longer than it needs to be.")
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "short": short,
            "long": long
        }
        r = requests.post(self.url + "/locations", headers=headers, json=data)
        return r.json()

    def updateLocation(self, locationid, short=None, long=None):
        data = {}
        if short:
            if len(short) > 4:
                raise LocationShortTooLong("Your short location name is much longer than it needs to be.")
            data['short'] = short
        if long:
            data['long'] = long
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.put(self.url + "/locations/" + str(locationid), headers=headers, json=data)
        return r.json()

    def removeLocation(self, locationid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/locations/" + str(locationid), headers=headers)
        return r.json()

    #   Servers

    def listServers(self):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers", headers=headers)
        return r.json()

    def getServer(self, serverid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(serverid), headers=headers)
        return r.json()

    def getServerByExternalID(self, extid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/external/" + str(extid), headers=headers)
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

        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.put(self.url + "/servers/" + str(serverid) + "/details", headers=headers, json=data)
        return r.json()

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
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.put(self.url + "/servers/" + str(serverid) + "/build", headers=headers, json=data)
        return r.json()

    def updateServerStartup(self, startup, egg, image, environment: dict=None, skip_scripts=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "startup": startup,
            "egg": egg,
            "image": image,
            "skip_scripts": skip_scripts
        }
        if enviroment:
            data['environment'] = enviroment

        r = requests.put(self.url + "/servers/" + str(serverid) + "/startup", headers=headers, json=data)
        return r.json()

    def createServer(self, name, userid, eggid, image, startup, enviroment: dict, limits: dict, feature_limits: dict, allocation: dict):
        if "databases" not in feature_limits:
            raise MissingData("You must specify databases. 'databases': 2")
        if "backups" not in feature_limits:
            raise MissingData("You must specify backups. 'backups': 2")
        if "default" not in allocation:
            raise MissingData("You must specify a default allocation. 'default': 2")

        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            'name': name,
            "user": userid,
            "egg": eggid,
            "docker_image": image,
            "startup": startup,
            "enviroment": enviroment,
            "limits": limits,
            "feature_limits": feature_limits,
            "allocation": allocation
        }
        r = requests.post(self.url + "/servers", headers=headers, json=data)
        return r.json()

    def suspendServer(self, serverid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.post(self.url + "/servers/" + str(serverid) + "/suspend", headers=headers)
        return r.json()

    def suspendServer(self, serverid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.post(self.url + "/servers/" + str(serverid) + "/unsuspend", headers=headers)
        return r.json()

    def reinstallServer(self, serverid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.post(self.url + "/servers/" + str(serverid) + "/reinstall", headers=headers)
        return r.json()

    def deleteServer(self, serverid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/servers/" + str(serverid), headers=headers, json=data)
        return r.json()

    def forceDeleteServer(self, serverid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/servers/" + str(serverid) + "/force", headers=headers, json=data)
        return r.json()

    #   Server Databases

    def listServerDatabases(self, serverid, include_pass_host=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(serverid) + f"/databases{'?include=password,host' if include_pass_host else ''}", headers=headers, json=data)
        return r.json()

    def getServerDBDetails(self, serverid, db_id, include_pass_host=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + "/servers/" + str(serverid) + f"/databases/" + str(db_id) + f"{'?include=password,host' if include_pass_host else ''}", headers=headers, json=data)
        return r.json()

    def createServerDatabase(self, db, remote="%", host=None):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        data = {
            "database": db,
            "remote": remote,
        }
        if host:
            data['host'] = host
        r = requests.post(self.url + "/servers/" + str(serverid) + "/databases", headers=headers, json=data)
        return r.json()

    def resetServerDBPassword(self, serverid, dbid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.post(self.url + "/servers/" + str(serverid) + "/databases/" + str(db_id) + "/reset-password", headers=headers)
        return r.json()

    def removeServerDB(self, serverid, dbid):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.delete(self.url + "/servers/" + str(serverid) + "/databases/" + str(db_id), headers=headers)
        return r.json()

    #   Nests

    def listNests(self, include_params=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + f"/nests{'?include=eggs,servers' if include_params else ''}", headers=headers)
        return r.json()

    def getNest(self, nestid, include_params=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + f"/nests/{nestid}{'?include=eggs,servers' if include_params else ''}", headers=headers)
        return r.json()

    def getNestEggs(self, nestid, include_params=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + f"/nests/{nestid}{'?include=nest,servers,config,script,variables' if include_params else ''}", headers=headers)
        return r.json()

    def getNestEgg(self, nestid, eggid, include_params=False):
        headers = {
            "Authorization": "Bearer {}".format(self.api_key),
            "Accept": "application/json",
            "Content-type": "application/json"
        }
        r = requests.get(self.url + f"/nests/{nestid}/eggs/{eggid}{'?include=nest,servers,config,script,variables' if include_params else ''}", headers=headers)
        return r.json()


if __name__ == "__main__":
    print("I dont run. No use in trying to make me lol")
