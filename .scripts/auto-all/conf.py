# script.py

INSTANCE_NAME = "haproxy"
INSTANCE_ZONE = "europe-west8-a"
HAPROXY_USER = "root"
PROJECT_ID = "gdg-ctf-2022"

STATS_PORT = 8080
STATS_USER = "admin"
STATS_PASSWORD = "9IIZHx53FATnUtJVTVcc"
DOMAIN_NAME = "chal.ctf.gdgalgiers.com"
HAPROXY_ROOT = "/etc/haproxy"
HAPROXY_MAPS_ROOT = f"{HAPROXY_ROOT}/maps"
HTTP_HOSTS_MAP = "http-hosts.map"
SNI_MAP = "sni.map"
HTTP_HOSTS_MAP_PATH = f"{HAPROXY_MAPS_ROOT}/{HTTP_HOSTS_MAP}"
SNI_MAP_PATH = f"{HAPROXY_MAPS_ROOT}/{SNI_MAP}"
SSL_CERTIFICATE_PATH = f"/etc/haproxy/{DOMAIN_NAME}.pem"
NODES = [
    {
        "name": "node1",
        "ip": "10.156.0.12"
    },
]
HTTP_TYPE = "http"
TCP_TYPE = "tcp"
CHALLENGES_JSON_PATH = "config/chals.json"
TEMPLATES_DIR = "templates"
HAPROXY_CFG = "haproxy.cfg"
HAPROXY_CONFIG_DIR = "config/haproxy"
DEPLOY = True
HELM_CHART_REPO = f"oci://europe-west3-docker.pkg.dev/{PROJECT_ID}/gdg-ctf-helm-repo/ctf-challenge-chart"
HELM_CHART_VERSION = "0.1.0"
HELM_REGISTRY = "https://europe-west3-docker.pkg.dev"
# IP blacklisting
IP_BAN_MINUTES = 2 # 2 minutes
CONN_RATE_SECONDS = 30 # 30 seconds
CONNS_PER_RATE = 50 # allow at most 50 connections in a 30s window (per IP)
CONCUR_CONNS = 25 # allow at most 25 concurrent connections (per IP)

# CTFd decay
DECAY = 50

MAX_NODES = 14
NODES_FQDN = "gke-nodes.internal"
CTFD_LINK = "https://ctf.gdgalgiers.com"

# challenge.py

NODEPORT_START = 30000
PORT_MOD = 1000
PORTS_PATH = "config/ports.yml"
YML_FILE = "challenge.yml"
INDENT = 4
CHAL_DIRS = {
    "crypto",
    "forensics",
    "jail",
    "linux",
    "misc",
    "osint",
    "pwn",
    "reverse",
    "web",
}
DEBUG = True
AUTOBAN_DEFAULT = False
FW_PRIORITY = 1000
FW_SOURCE_RANGES = "0.0.0.0/0"
FW_TARGET_TAGS = "haproxy"
FW_SKIP_CHECK = False
DYNAMIC_CHAL_TYPE = "dynamic"
DOCKER_CHAL_TYPE = "docker"
PORT_PLACE_HOLDER = "${PORT}"
PROJECT_ID_PLACE_HOLDER = "${PROJECT_ID}"
# Override existing challenges in chals.json
OVERRIDE_CHALS_JSON = True
# Override existing firewall rules
OVERRIDE_FW = False
DEFAULT_DELETE_FW = False
GCR_REPO = f"gcr.io/{PROJECT_ID}"
DOCKERFILE_DIRS = {
    ".",
    "challenge",
    "app",
}
DOCKERFILE_NAME = "Dockerfile"

# ctfcli
CTFCLI_CMD = "ctf"
CTFCLI_CHAL_TRACKER_PATH = "config/ctfcli_chals.json"
CHSTATE_VISIBLE = "visible"
CHSTATE_HIDDEN = "hidden"
