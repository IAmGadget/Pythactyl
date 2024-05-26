import requests

from Pythactyl import Admin

HEADERS = {
    "Accept": "application/json",
    "Content-type": "application/json"
}

class User:
    def __init__(self, resp: dict):
        self.email = resp["email"]
        self.username = resp["username"]
        self.fname = resp["first_name"]
        self.lname = resp["last_name"]
        self.lang = resp["language"]
        self.admin = resp["root_admin"]
        self.id = resp["uuid"]
        self.twofactor = resp["2fa"]
        self.type = "User"
        self.created_at = resp["created_at"]

    def __repr__(self):
        return f"<Object User: {self.username}>"

class Node:
    def __init__(self, resp):
        self.id = resp['id']
        self.uuid = resp['uuid']
        self.public = resp['public']
        self.name = resp['name']
        self.description = resp['description']
        self.location_id = resp['location_id']
        self.fqdn = resp['fqdn']
        self.scheme = resp['scheme']
        self.behind_proxy = resp['behind_proxy']
        self.maintenance_mode = resp['maintenance_mode']
        self.memory = resp['memory']
        self.memory_overallocate = resp['memory_overallocate']
        self.disk = resp['disk']
        self.disk_overallocate = resp['disk_overallocate']
        self.upload_size = resp['upload_size']
        self.daemon_listen = resp['daemon_listen']
        self.daemon_sftp = resp['daemon_sftp']
        self.daemon_base = resp['daemon_base']
        self.created_at = resp['created_at']
        self.updated_at = resp['updated_at']
        self.allocated_resources = resp['allocated_resources']
    def __repr__(self):
        return f"<Object Node: {self.name}>"

class NodeConfig:
    def __init__(self, resp: dict):
        self.debug = resp['debug']
        self.uuid = resp['uuid']
        self.token_id = resp['token_id']
        self.token = resp['token']
        self.api_host = resp['api']['host']
        self.api_port = resp['api']['port']
        self.api_sll = resp['api']['ssl']['enabled']
        self.sll_cert = resp['api']['ssl']['cert']
        self.ssl_key = resp['api']['ssl']['key']
        self.api_upload_limit = resp['api']['upload_limit']
        self.system = resp['system']['data']
        self.sftp = resp['system']['sftp']['bind_port']
        self.allowed_mounts = resp['allowed_mounts']
        self.remote_uri = resp['remote']

class Allocation:
    def __init__(self, resp: dict):
        self.id = resp['id']
        self.ip = resp['ip']
        self.alias = resp['alias']
        self.port: int = resp['port']
        self.notes: str = resp['notes']
        self.assigned: bool = resp['assigned']

class Key:
    def __init__(self, identifier=None, description=None, allowed_ips=None, lastused=None, created_at=None, token=None):
        self.id = identifier
        self.description = description
        self.allowed_ips = allowed_ips
        self.lastusedat = lastused
        self.created_at = created_at
        self.token = token

    def __repr__(self):
        return f"<{self.token if self.token else self.id}>"

class Location:
    def __init__(self, resp: dict):
        self.id = resp['id']
        self.short = resp['short']
        self.long = resp['long']
        self.created_at = resp['created_at']
        self.updated_at = resp['updated_at']


class Server:
    def __init__(self, resp):
        self.id = resp['id']
        self.identifier = resp['identifier']
        self.uuid = resp['uuid']
        self.name = resp['name']
        self.node = resp['node']
        self.description = resp['description']
        self.memory = resp['limits']['memory']
        self.swap = resp['limits']['swap']
        self.disk_space = resp['limits']['disk']
        self.io = resp['limits']['io']
        self.cpu = resp['limits']['cpu']
        self.thread = resp['limits']['threads']
        self.oom_disabled = resp['limits']['oom_disabled']

        self.databases = resp['feature_limits']['databases']
        self.allocation = resp['feature_limits']['allocations']
        self.backups = resp['feature_limits']['backups']
        self.owner_id = resp['user']
        self.node_id = resp['node']
        self.allocation_id = resp['allocation']
        self.egg_id = resp['egg']

        self.startup_command = resp['container']['startup_command']
        self.image = resp['container']['image']
        self.installed = resp['container']['installed']
        self.enviroment = resp['container']['environment']
        self.created_at = resp['created_at']
        self.updated_at = resp['updated_at']
        self.suspended = resp['suspended']


class SFTP:
    def __init__(self, ip=None, port=None):
        self.ip = ip
        self.port = port

class ServerLimits:
    def __init__(self, memory=None, swap=None, disk=None, io=None, cpu=None):
        self.memory = memory
        self.swap = swap
        self.disk = disk
        self.io = io
        self.cpu = cpu

class FeatureLimits:
    def __init__(self, databases=None, allocations=None, backups=None):
        self.databases = databases
        self.allocations = allocations
        self.backups = backups

class Database:
    def __init__(self, resp):
        self.id = resp['id']
        self.server_id = resp['server']
        self.node_id = resp['host']
        self.database = resp['database']
        self.db_user = resp['username']
        self.remote = resp['remote']
        self.max_connections = resp['max_connections']
        self.root_pass = resp['relationships']['password']['attributes']['password']
        self.host_id = resp['host']['attributes']['id']
        self.host_port =resp['host']['attributes']['port']
        self.host_username = resp['host']['attributes']['username']
        self.host_node_id = resp['host']['attributes']['node']
        self.created_at = resp['host']['attributes']['created_at']
        self.updated_at = resp['host']['attributes']['updated_at']

class Nest:
    def __init__(self, resp):
        self.id = resp['id']
        self.uuid = resp['uuid']
        self.author = resp['author']
        self.name = resp['name']
        self.description = resp['description']
        self.created_at = resp['created_at']
        self.updated_at = resp['updated_at']

class EggVariable:
    def __init__(self, resp):
        self.id = resp['id']
        self.egg_id = resp['egg_id']
        self.name = resp['name']
        self.description = resp['description']
        self.env_variable = resp['env_variable']
        self.default_value = resp['default_value']
        self.user_viewable = resp['user_viewable']
        self.rules = resp['rules']
        self.created_at = resp['created_at']
        self.updated_at = resp['updated_at']

class Egg:
    def __init__(self, resp: dict):
        self.id = resp['id']
        self.uuid = resp['uuid']
        self.name = resp['name']
        self.nest = resp['nest']
        self.author = resp['author']
        self.description = resp['description']
        self.docker_image = resp['docker_image']
        self.stop_command = resp['config']['stop']
        self.startup_commmad = resp['startup']
        self.priveleged = resp['script']['privileged']
        self.install_script = resp['script']['install']
        self.container = resp['script']['container']
        if resp.get("relationships"):
            self.variables = []
            for x in resp['relationships']['variables']['data']:
                a = EggVariable(x['attributes'])
                self.variables.append(a)


class Relationship:
    def __init__(self, id=None, ip=None, ip_alias=None, port=None, notes=None, default=None):
        self.id = id
        self.ip = ip
        self.ip_alias = ip_alias
        self.port = port
        self.notes = notes
        self.default = default