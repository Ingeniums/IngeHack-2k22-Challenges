from genericpath import isfile
import yaml
import json
from conf import *
import os
from sys import stderr
import subprocess

# Track if we're logged in to Helm registry or not
LOGGED_IN = False

class Challenge:
    def __init__(self, name=None, type=None, category=None, autoban=None, path=None, nodeport=None, deployed=None, wave=None):
        self.name = name
        self.subdomain = name
        self.type = type
        self.category = category
        self.autoban = autoban
        self.path = path
        self.nodeport = nodeport
        self.port = Challenge.port_from_nodeport(nodeport)
        self.deployed = deployed
        self.wave = wave

    def __repr__(self):
        return "%s(name=%r, category=%r, type=%r)" % (
            self.__class__.__name__, self.name, self.category, self.type)

    def todict(self):
        return {
            self.name: {
                "name": self.name,
                "subdomain": self.subdomain,
                "type": self.type,
                "category": self.category,
                "autoban": self.autoban,
                "path": self.path,
                "nodeport": self.nodeport,
                "port": self.port,
            }
        }

    @staticmethod
    def nodeport_from_port(port):
        if port is None:
            return None
        else:
            return port - PORT_MOD + NODEPORT_START

    @staticmethod
    def port_from_nodeport(nodeport):
        if nodeport is None:
            return None
        else:
            return nodeport + PORT_MOD - NODEPORT_START

class DeployException(Exception):
    pass

class HelmDeployException(DeployException):
    pass
class FirewallDeployException(DeployException):
    pass

def ymlpath(chalpath):
    return f"{chalpath}/{YML_FILE}"

def log(msg, debug=DEBUG):
    debug and print(msg, file=stderr)

# this if for any challenge
# chalpath as {category}/{challenge_name}
def load_any_chal(chalpath, quiet=False):
    ymlfile = ymlpath(chalpath)

    if not os.path.isfile(ymlfile):
        raise DeployException(f"No such file '{ymlfile}'")

    with open(ymlfile) as f:
        chal_data = yaml.safe_load(f)
        name = chal_data['name']
        not quiet and log(f"[*] Loading challenge '{name}'")
        chal = Challenge(
            name=chal_data.get("deployment", {"name": name})['name'],
            type=chal_data.get("deployment", {"type": None})['type'],
            category=chal_data['category'],
            autoban=chal_data.get("deployment", {"autoban": None}).get('autoban'),
            path=chalpath,
            nodeport=chal_data.get("deployment", {"nodePort": None}).get('nodePort'),
            deployed=chal_data.get("deployment", {"deployed": None}).get('deployed'),
            wave=chal_data.get("wave", None),
        )
    return chal

# this if for dynamic deployable challenges
# chalpath as {category}/{challenge_name}
def load_chal(chalpath, warn=True):
    ymlfile = ymlpath(chalpath)

    if not os.path.isfile(ymlfile):
        raise DeployException(f"No such file '{ymlfile}'")

    with open(ymlfile) as f:
        chal_data = yaml.safe_load(f)
        name = chal_data['name']
        log(f"[*] Loading challenge '{name}'")
        if not chal_data.get("deployment"):
            warn and log(f"[!] Skipping challenge '{name}' as it doesn't contain a 'deployment' section")
            chal = None
        elif chal_data["type"] != DYNAMIC_CHAL_TYPE:
            warn and log(f"[!] Skipping challenge '{name}' as type is set to '{chal_data['type']}' (not '{DYNAMIC_CHAL_TYPE}')")
            chal = None
        else:
            chal = Challenge(
                chal_data["deployment"]["name"],
                chal_data["deployment"]["type"],
                chal_data["category"],
                chal_data["deployment"].get("autoban", AUTOBAN_DEFAULT),
                chalpath,
                chal_data["deployment"].get("nodePort", None),
                chal_data["deployment"].get("deployed", False),
                chal_data.get("wave", None),
            )
    return chal

def update_chal_data(chal_data, chal: Challenge):
    if chal_data["type"] == DYNAMIC_CHAL_TYPE:
        chal_data["extra"]["decay"] = DECAY
        if chal is not None:
            if chal_data.get("connection_info") and chal.port is not None and PORT_PLACE_HOLDER in chal_data["connection_info"]:
                chal_data["connection_info"] = chal_data["connection_info"].replace(PORT_PLACE_HOLDER, f"{chal.port}")
                log(f"[*] Updated connection info for '{chal.name}': {chal_data['connection_info']}")
            if chal.nodeport is not None:
                chal_data["deployment"]["nodePort"] = chal.nodeport
            chal_data["deployment"]["deployed"] = chal.deployed
    elif chal_data["type"] == DOCKER_CHAL_TYPE:
        if chal_data.get("docker_image") and PROJECT_ID_PLACE_HOLDER in chal_data['docker_image']:
            chal_data['docker_image'] = chal_data['docker_image'].replace(PROJECT_ID_PLACE_HOLDER, PROJECT_ID)

def dump_chal(chal: Challenge, chalpath):
    with open(ymlpath(chalpath)) as f:
        chal_data = yaml.safe_load(f)
    with open(ymlpath(chalpath), 'w') as f:
        update_chal_data(chal_data, chal)
        yaml.safe_dump(chal_data, f, default_flow_style=False)

def load_chals_json():
    with open(CHALLENGES_JSON_PATH) as f:
        chals_json = json.load(f)
    return chals_json

def dump_chals_json(chals, override=OVERRIDE_CHALS_JSON):
    if len(chals) > 0:
        existing_chals = load_chals_json()
        with open(CHALLENGES_JSON_PATH, 'w') as f:
            new_chals = {}
            for chal in chals:
                new_chals.update(chal.todict())
            if override:
                for chal_name in new_chals:
                    if chal_name in existing_chals:
                        log(f"[!] Overriding challenge '{chal_name}' in '{CHALLENGES_JSON_PATH}'")
                data = existing_chals | new_chals
            else:
                for chal_name in new_chals:
                    if chal_name in existing_chals:
                        log(f"[!] Skipping challenge '{chal_name}' as it already exists in '{CHALLENGES_JSON_PATH}'")
                data = new_chals | existing_chals
            json.dump(data, f, indent=INDENT)
        log(f"[*] Challenges added to {CHALLENGES_JSON_PATH}")
    else:
        log(f"[*] No new challenges to add to '{CHALLENGES_JSON_PATH}'")

def remove_chal_chals_json(chal: Challenge):
    if chal is not None:
        existing_chals = load_chals_json()
        if chal.name not in existing_chals:
            log(f"[!] Cannot remove '{chal.name}' from '{CHALLENGES_JSON_PATH}' as it does not exist")
        else:
            with open(CHALLENGES_JSON_PATH, 'w') as f:
                existing_chals.pop(chal.name)
                json.dump(existing_chals, f, indent=INDENT)
            log(f"[*] '{chal.name}' removed from '{CHALLENGES_JSON_PATH}'")

def load_ports():
    with open(PORTS_PATH) as f:
        ports = yaml.safe_load(f)
    return ports

def dump_ports(ports):
    with open(PORTS_PATH, 'w') as f:
        yaml.safe_dump(ports, f, default_flow_style=False)

def assign_port(chal: Challenge, ports):
    if chal.nodeport is not None:
        log(f"[!] Ports (port={chal.port}, nodeport={chal.nodeport}) were already set for challenge '{chal.name}'")
    else:
        port = ports[chal.category]
        nodeport = Challenge.nodeport_from_port(port)
        chal.port = port
        chal.nodeport = nodeport
        log(f"[*] Ports (port={port}, nodeport={nodeport}) set to challenge '{chal.name}'")
        ports[chal.category] += 1

def get_chalpaths(wave=None, reverse=False):
    chalpaths = []
    for category in CHAL_DIRS:
        if os.path.isdir(category):
            for name in os.listdir(category):
                chalpath = f"{category}/{name}"
                if os.path.isdir(chalpath) and os.path.isfile(ymlpath(chalpath)):
                    if wave is not None:
                        chal = load_any_chal(chalpath, quiet=True)
                        if reverse ^ (chal.wave == wave):
                            chalpaths.append(chalpath)
                    else:
                        chalpaths.append(chalpath)
    return chalpaths

# def update_chal(chalpath):
#     chals = update_chals([chalpath])
#     if len(chals) > 0:
#         return chals[0]
#     else:
#         return None

def _deploy_chal(chalpath, ports, build, deploy, createfw, push_ctfd, overridefw=OVERRIDE_FW):
    global LOGGED_IN

    chal = load_chal(chalpath)
    if chal is None:
        if push_ctfd:
            ctfcli_push(chalpath, update=True)
    else:
        try:
            assign_port(chal, ports)
            if build:
                _build_image(chal)
            if deploy:
                if chal.deployed:
                    log(f"[!] Challenge {chal.name} has already been deployed (deployment.deployed is set to true)")
                else:
                    if not LOGGED_IN:
                        if not helm_login():
                            raise HelmDeployException("Could not login to helm registry")
                        LOGGED_IN = True
                    dump_chal(chal, chalpath)
                    if not helm_install(chal):
                        raise HelmDeployException(f"Could not deploy '{chal.name}' to Kubernetes cluster")
                    chal.deployed = True
            if _istcp(chal) and createfw:
                rule = _fw_rule_name(chal)
                if _fw_rule_exists(chal):
                    if overridefw:
                        log(f"[!] Firewall rule '{rule}' already exists but it will be overriden")
                        if not _delete_fw_rule(chal):
                            raise FirewallDeployException(f"Could not delete firewall rule '{rule}'")
                        if not _create_fw_rule(chal):
                            raise FirewallDeployException(f"Could not create firewall rule '{rule}'")
                    else:
                        log(f"[!] Firewall rule '{rule}' already exists, it will be enabled if not already")
                        if not _enable_fw_rule(chal):
                            raise FirewallDeployException(f"Could not enable firewall rule '{rule}'")
                else:
                    if not _create_fw_rule(chal):
                        raise FirewallDeployException(f"Could not create firewall rule '{rule}'")
            dump_chal(chal, chalpath)
            if push_ctfd:
                ctfcli_push(chal.path, update=False)
        except HelmDeployException as e:
            raise e
        except FirewallDeployException as e:
            log(f"[-] {e}")
            if deploy and chal.deployed and LOGGED_IN:
                if not helm_uninstall(chal):
                    raise HelmDeployException(f"[!] Could not undeploy '{chal.name}' from Kubernetes cluster")
            raise e
    return chal

def undeploy_chal(chalpath, deletefw=DEFAULT_DELETE_FW):
    global LOGGED_IN

    chal = load_chal(chalpath)
    if chal is not None:
        if chal.deployed:
            if not LOGGED_IN:
                if not helm_login():
                    raise HelmDeployException("Could not login to helm registry")
                LOGGED_IN = True
            if not helm_uninstall(chal):
                raise HelmDeployException(f"[!] Could not undeploy '{chal.name}' from Kubernetes cluster")
            chal.deployed = False
            rule = _fw_rule_name(chal)
            if _istcp(chal):
                if not _fw_rule_exists(chal):
                    log(f"[!] Firewall rule '{rule}' does not exist")
                else:
                    if deletefw:
                        if not _delete_fw_rule(chal):
                            raise FirewallDeployException(f"Could not delete firewall rule '{rule}'")
                    else:
                        if not _disable_fw_rule(chal):
                            raise FirewallDeployException(f"Could not disable firewall rule '{rule}'")
            dump_chal(chal, chalpath)
        else:
            log(f"[!] Challenge {chal.name} was not already deployed (deployment.deployed is set to false)")
        remove_chal_chals_json(chal)
    return chal

def dump(chals, ports):
    dump_chals_json(chals)
    dump_ports(ports)

def deploy_chals(chalpaths, build, deploy, createfw, push_ctfd):
    ports = load_ports()
    chals = []
    ex = None
    try:
        for chalpath in chalpaths:
            chal = _deploy_chal(chalpath, ports, build, deploy, createfw, push_ctfd)
            if chal is not None:
                chals.append(chal)
    except DeployException as e:
        ex = e
    finally:
        dump(chals, ports)
    if ex is not None:
        raise ex
    return chals

def undeploy_chals(chalpaths, deletefw=DEFAULT_DELETE_FW):
    for chalpath in chalpaths:
        undeploy_chal(chalpath, deletefw)

# Helm

def helm_login():
    log(f"[*] Login into Helm registry")
    return os.system(f'gcloud auth print-access-token | helm registry login -u oauth2accesstoken --password-stdin {HELM_REGISTRY}') == 0

def helm_install(chal: Challenge):
    # helm install ${challenge_name} oci://europe-west3-docker.pkg.dev/gdg-ctf-2022/gdg-ctf-helm-repo/ctf-challenge-chart --version 0.1.0 -f challenge.yml 
    log(f"[*] Deploying '{chal.name}' to Kubernetes cluster")
    return subprocess.run(["helm", "install", chal.name, HELM_CHART_REPO, "--version", HELM_CHART_VERSION, "-f", ymlpath(chal.path)]).returncode == 0

def helm_uninstall(chal: Challenge):
    log(f"[*] Undeploying '{chal.name}' from Kubernetes cluster")
    return subprocess.run(["helm", "uninstall", chal.name]).returncode == 0

# Firewall

# For fw functions, it is assumed that the challenge is of type TCP

def _fw_rule_name(chal: Challenge):
    return f"allow-{chal.category}-{chal.name}"

def _istcp(chal: Challenge):
    return chal.type == TCP_TYPE

def _fw_rule_exists(chal: Challenge):
    rule = _fw_rule_name(chal)
    return subprocess.run(["gcloud", "compute", "firewall-rules", "describe", rule], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def _create_fw_rule(chal: Challenge):
    rule = _fw_rule_name(chal)
    log(f"[*] Creating firewall rule '{rule}'")
    return subprocess.run(["gcloud", "compute", "firewall-rules", "create", rule, "--direction=INGRESS", f"--priority={FW_PRIORITY}",  "--network=default", "--action=ALLOW", f"--rules=tcp:{chal.port}", f"--source-ranges={FW_SOURCE_RANGES}", f"--target-tags={FW_TARGET_TAGS}"]).returncode == 0

def _delete_fw_rule(chal: Challenge):
    rule = _fw_rule_name(chal)
    log(f"[*] Deleting firewall rule '{rule}'")
    return subprocess.run(["gcloud", "compute", "firewall-rules", "delete", rule]).returncode == 0

def _enable_fw_rule(chal: Challenge):
    rule = _fw_rule_name(chal)
    log(f"[*] Enabling firewall rule '{rule}'")
    return subprocess.run(["gcloud", "compute", "firewall-rules", "update", rule, "--no-disabled"]).returncode == 0

def _disable_fw_rule(chal: Challenge):
    rule = _fw_rule_name(chal)
    log(f"[*] Disabling firewall rule '{rule}'")
    return subprocess.run(["gcloud", "compute", "firewall-rules", "update", rule, "--disabled"]).returncode == 0

# "Exported" functions

def create_fw(chalpath, skipcheck=FW_SKIP_CHECK):
    chal = load_chal(chalpath)
    if chal is None:
        return None
    if not _istcp(chal):
        log(f"[!] '{chal.name}' is a '{chal.type}' challenge (not '{TCP_TYPE}'), no firewall rule to create")
    else:
        if not skipcheck and _fw_rule_exists(chal):
            log(f"[!] Firewall rule already exists for '{chal.name}'")
        else:
            return _create_fw_rule(chal)

def delete_fw(chalpath, skipcheck=FW_SKIP_CHECK):
    chal = load_chal(chalpath)
    if chal is None:
        return None
    if not _istcp(chal):
        log(f"[!] '{chal.name}' is a '{chal.type}' challenge (not '{TCP_TYPE}'), no firewall rule to delete")
    else:
        if not skipcheck and not _fw_rule_exists(chal):
            log(f"[!] No firewall rule found for '{chal.name}'")
        else:
            return _delete_fw_rule(chal)

def enable_fw(chalpath, skipcheck=FW_SKIP_CHECK):
    chal = load_chal(chalpath)
    if chal is None:
        return None
    if not _istcp(chal):
        log(f"[!] '{chal.name}' is a '{chal.type}' challenge (not '{TCP_TYPE}'), no firewall rule to enable")
    else:
        if not skipcheck and not _fw_rule_exists(chal):
            log(f"[!] No firewall rule found for '{chal.name}'")
        else:
            return _enable_fw_rule(chal)

def disable_fw(chalpath, skipcheck=FW_SKIP_CHECK):
    chal = load_chal(chalpath)
    if chal is None:
        return None
    if not _istcp(chal):
        log(f"[!] '{chal.name}' is a '{chal.type}' challenge (not '{TCP_TYPE}'), no firewall rule to disable")
    else:
        if not skipcheck and not _fw_rule_exists(chal):
            log(f"[!] No firewall rule found for '{chal.name}'")
        else:
            return _disable_fw_rule(chal)

# Build

def _build_image(chal: Challenge):
    if chal is not None:
        for dir in DOCKERFILE_DIRS:
            dockerfile = f"{chal.path}/{dir}/{DOCKERFILE_NAME}"
            if os.path.isfile(dockerfile):
                return subprocess.run(["gcloud", "builds", "submit", "--tag", f"{GCR_REPO}/{chal.name}"], cwd=f"{chal.path}/{dir}").returncode == 0
        else:
            raise DeployException(f"Cannot find {DOCKERFILE_NAME} in {chal.path}")

def build_image(chalpath):
    chal = load_chal(chalpath)
    return _build_image(chal)

# ssh/scp

# scp local to remote
def gcloud_scp_l2r(localpath, remotepath, user, instance, zone):
    return subprocess.run(["gcloud", "compute", "scp", localpath, f"{user}@{instance}:{remotepath}", "--zone", zone]).returncode == 0

# scp remote to local
def gcloud_scp_r2l(remotepath, localpath, user, instance, zone):
    return subprocess.run(["gcloud", "compute", "scp", f"{user}@{instance}:{remotepath}", localpath, "--zone", zone]).returncode == 0

# run command through ssh
def gcloud_ssh_cmd(user, instance, zone, cmd):
    return subprocess.run(["gcloud", "compute", "ssh", "--zone", zone, f"{user}@{instance}", f"--command={cmd}"]).returncode == 0

# ctfcli

def _load_ctfcli_tracker():
    if not os.path.isfile(CTFCLI_CHAL_TRACKER_PATH):
        raise DeployException(f"Cannot open ctfcli challenge tracker file: '{CTFCLI_CHAL_TRACKER_PATH}'")
    with open(CTFCLI_CHAL_TRACKER_PATH) as f:
        chalpaths = json.load(f)
    return chalpaths

def _ctfcli_chal_exists(chalpath):
    chalpaths = _load_ctfcli_tracker()
    return chalpath in chalpaths

def _ctfcli_track_chal(chalpath):
    chalpaths = _load_ctfcli_tracker()
    if chalpath in chalpaths:
        log(f"[!] '{chalpath}' is already tracked in '{CTFCLI_CHAL_TRACKER_PATH}'")
    else:
        with open(CTFCLI_CHAL_TRACKER_PATH, "w") as f:
            chalpaths.append(chalpath)
            json.dump(chalpaths, f, indent=INDENT)

def _ctfcli_untrack_chal(chalpath):
    chalpaths = _load_ctfcli_tracker()
    if chalpath not in chalpaths:
        log(f"[!] '{chalpath}' is not tracked in '{CTFCLI_CHAL_TRACKER_PATH}'")
    else:
        with open(CTFCLI_CHAL_TRACKER_PATH, "w") as f:
            chalpaths.remove(chalpath)
            json.dump(chalpaths, f, indent=INDENT)

def _ctfcli_untrack_all():
    with open(CTFCLI_CHAL_TRACKER_PATH, "w") as f:
        json.dump([], f, indent=INDENT)

def _ctfcli_cmd(chalpath, cmd):
    return subprocess.run([CTFCLI_CMD, "challenge", cmd, chalpath]).returncode

def _ctfcli_plugin_chstate(chalpath, hide):
    action = "hide" if hide else "unhide"
    return subprocess.run([CTFCLI_CMD, "plugins", "chstate", action, chalpath]).returncode

# def _ctfcli_add(chalpath):
#     return _ctfcli_cmd(chalpath, "add")

def _ctfcli_install(chalpath):
    return _ctfcli_cmd(chalpath, "install")

def _ctfcli_sync(chalpath):
    return _ctfcli_cmd(chalpath, "sync")

def ctfcli_push(chalpath, update):
    if update:
        log(f"[*] Updating '{ymlpath(chalpath)}'")
        chal = load_chal(chalpath, warn=False)
        dump_chal(chal, chalpath)
    log(f"[*] Pushing '{chalpath}' to CTFd")
    if _ctfcli_chal_exists(chalpath):
        _ctfcli_sync(chalpath)
    else:
        _ctfcli_install(chalpath)
        _ctfcli_track_chal(chalpath)

def ctfcli_untrack(chalpath):
    log(f"[*] Untracking '{chalpath}'")
    return _ctfcli_untrack_chal(chalpath)

def ctfcli_untrack_all():
    log(f"[*] Untracking all challenges")
    return _ctfcli_untrack_all()

def ctfcli_chstate(chalpath, state):
    if state == CHSTATE_HIDDEN:
        hide = True
    elif state == CHSTATE_VISIBLE:
        hide = False
    else:
        raise DeployException(f"Invalid state '{state}'")
    return _ctfcli_plugin_chstate(chalpath, hide)
