import requests


class User:
    def __init__(self, resp: dict):
        self.id = resp["id"]
        self.email = resp["email"]
        self.username = resp["username"]
        self.fname = resp["first_name"]
        self.lname = resp["last_name"]
        self.lang = resp["language"]
        self.admin = resp["root_admin"] if resp.get("root_admin") else False
        self.id = resp["uuid"] if resp.get("uuid") else resp["id"]
        self.twofactor = resp["2fa"] if resp.get("2fa") else False
        self.type = "User"
        self.created_at = resp["created_at"] if resp.get("created_at") else None
        self.updated_at = resp["updated_at"] if resp.get("updated_at") else None

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
        self.id = resp['id'] if resp.get('id') else None
        self.identifier = resp['identifier'] if resp.get('identifier') else None
        self.uuid = resp['uuid'] if resp.get('uuid') else None
        self.name = resp['name'] if resp.get('name') else None
        self.node = resp['node'] if resp.get('node') else None
        self.description = resp['description'] if resp.get('description') else None
        self.memory = resp['limits']['memory'] if resp.get('limits') else None
        self.swap = resp['limits']['swap'] if   resp.get('limits') else None
        self.disk_space = resp['limits']['disk'] if resp.get('limits') else None
        self.io = resp['limits']['io'] if resp.get('limits') else None
        self.cpu = resp['limits']['cpu'] if resp.get('limits') else None
        self.thread = resp['limits']['threads'] if resp.get('limits') else None
        self.oom_disabled = resp['limits']['oom_disabled'] if resp.get('limits') else None

        self.databases = resp['feature_limits']['databases'] if resp.get('feature_limits') else None
        self.allocation = resp['feature_limits']['allocations'] if resp.get('feature_limits') else None
        self.backups = resp['feature_limits']['backups'] if resp.get('feature_limits') else None
        self.owner_id = resp['user'] if resp.get('user') else None
        self.node_id = resp['node'] if resp.get('node') else None
        self.allocation_id = resp['allocation'] if resp.get('allocation') else None
        self.egg_id = resp['egg'] if resp.get('egg') else None

        self.startup_command = resp['container']['startup_command'] if resp.get('container') else None
        self.image = resp['container']['image'] if resp.get('container') else None
        self.installed = resp['container']['installed'] if resp.get('container') else None
        self.enviroment = resp['container']['environment'] if resp.get('container') else None
        self.created_at = resp['created_at'] if resp.get('created_at') else None
        self.updated_at = resp['updated_at'] if resp.get('updated_at') else None
        self.suspended = resp['suspended'] if resp.get('suspended') else None
        self.is_owner = resp['server_owner'] if resp.get('server_owner') else False
    def __repr__(self):
        return f"{self.identifier}"
    def __str__(self):
        return f"{self.name} - {self.identifier}"

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