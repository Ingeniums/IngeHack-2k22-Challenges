#!/usr/bin/env python3

from conf import *
import jinja2
from os import path
import json
import re
from challenge import *
import argparse
import sys

SCRIPT_ROOT = path.dirname(__file__)
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(path.join(SCRIPT_ROOT, TEMPLATES_DIR)), trim_blocks=True, lstrip_blocks=True)
SUBDOMAIN_REGEX = "^[A-Za-z0-9](?:[A-Za-z0-9\-]{0,61}[A-Za-z0-9])?$"

def argument_parser():
    parser = argparse.ArgumentParser(description="Auto assign challenge ports, update HAProxy configuration and deploy challenges to Kubernetes")

    parser.add_argument("-c", "--challenges", metavar="CHALLENGE", nargs="*", help="Paths to challenges")
    parser.add_argument("-d", "--deploy", default=True, action="store_true", help="Assign port, deploy to HAProxy and Kubernetes, and create firewall rule (this is done by default)")
    parser.add_argument("-u", "--undeploy", action="store_true", help="Undeploy from HAProxy and Kubernetes, and disable or delete firewall rule (default is to disable)")
    parser.add_argument("--only-haproxy", action="store_true", help="Only update HAProxy configuration")
    parser.add_argument("-A", "--all", action="store_true", help="Apply to all challenges")
    parser.add_argument("--deploy-no-create-fw", action="store_true", help="Do not create firewall rule when using --deploy (default is to create)")
    parser.add_argument("--undeploy-delete-fw", action="store_true", help="Delete firewall rule when using --undeploy (default is to disable not delete)")
    parser.add_argument("--create-fw", action="store_true", help="Create firewall rule")
    parser.add_argument("--delete-fw", action="store_true", help="Delete firewall rule")
    parser.add_argument("--enable-fw", action="store_true", help="Enable firewall rule")
    parser.add_argument("--disable-fw", action="store_true", help="Disable firewall rule")
    parser.add_argument("--no-build", action="store_true", help="Do not build container image (default is to build)")
    parser.add_argument("--only-build", action="store_true", help="Only build container image")
    parser.add_argument("--only-push-ctfd", action="store_true", help="Only push to CTFd")
    parser.add_argument("--no-push-ctfd", action="store_true", help="Do not push to CTFd (default is to push)")
    parser.add_argument("--only-ctfcli-untrack", action="store_true", help="Untrack from ctfcli tracker")
    parser.add_argument("-s", "--state", choices=[CHSTATE_HIDDEN, CHSTATE_VISIBLE], help="Change visibility state on CTFd")
    parser.add_argument("-w", "--wave", metavar="WAVE", type=int, help="Apply to specified wave of challenges")
    parser.add_argument("--not-wave", metavar="WAVE", type=int, help="Apply to challenges not of specified wave")

    return parser

def parse_chals(filename):
    with open(filename) as f:
        challenges = json.load(f)
    for chal in challenges.values():
        subdomain = chal["subdomain"] or chal["name"]
        if not re.match(SUBDOMAIN_REGEX, subdomain):
            raise ValueError(f"'{subdomain}' does not match subdomain regular expression")
    return challenges.values()

def haproxy_cfg(filename, challenges, directory):
    filepath = f"{directory}/{filename}"
    if path.exists(filepath):
        log(f"[!] Warning: '{filepath}' already exists")

    template = JINJA_ENV.get_template(f"{filename}.j2")
    content = template.render({
        "challenges": challenges,
        "HTTP_HOSTS_MAP_PATH": HTTP_HOSTS_MAP_PATH,
        # "SNI_MAP_PATH": SNI_MAP_PATH,
        "TCP_TYPE": TCP_TYPE,
        "HTTP_TYPE": HTTP_TYPE,
        "NODES": NODES,
        "STATS_PORT": STATS_PORT,
        "STATS_USER": STATS_USER,
        "STATS_PASSWORD": STATS_PASSWORD,
        # "SSL_CERTIFICATE_PATH": SSL_CERTIFICATE_PATH,
        "IP_BAN_MINUTES": IP_BAN_MINUTES,
        "CONN_RATE_SECONDS": CONN_RATE_SECONDS,
        "CONNS_PER_RATE": CONNS_PER_RATE,
        "CONCUR_CONNS": CONCUR_CONNS,
        "MAX_NODES": MAX_NODES,
        "NODES_FQDN": NODES_FQDN,
        "CTFD_LINK": CTFD_LINK,
    })
    with open(filepath, 'w') as f:
        f.write(content)

def hosts_map(filename, challenges, directory):
    filepath = f"{directory}/{filename}"
    if path.exists(filepath):
        log(f"[!] Warning: '{filepath}' already exists")

    template = JINJA_ENV.get_template(f"{filename}.j2")
    content = template.render({
        "challenges": challenges,
        "HTTP_TYPE": HTTP_TYPE,
        "DOMAIN_NAME": DOMAIN_NAME
    })
    with open(filepath, 'w') as f:
        f.write(content)

def update_haproxy():
    # Generate HAProxy config files
    challenges = parse_chals(CHALLENGES_JSON_PATH)
    haproxy_cfg(HAPROXY_CFG, challenges, HAPROXY_CONFIG_DIR)
    hosts_map(HTTP_HOSTS_MAP, challenges, HAPROXY_CONFIG_DIR)
    # hosts_map(SNI_MAP, challenges, directory)

    # Copy the files to remote server and restart HAProxy
    gcloud_scp_l2r(f"{HAPROXY_CONFIG_DIR}/{HAPROXY_CFG}", HAPROXY_ROOT, HAPROXY_USER, INSTANCE_NAME, INSTANCE_ZONE)
    gcloud_scp_l2r(f"{HAPROXY_CONFIG_DIR}/{HTTP_HOSTS_MAP}", HAPROXY_MAPS_ROOT, HAPROXY_USER, INSTANCE_NAME, INSTANCE_ZONE)
    gcloud_ssh_cmd(HAPROXY_USER, INSTANCE_NAME, INSTANCE_ZONE, "systemctl restart haproxy; systemctl status haproxy")

if __name__ == "__main__":
    parser = argument_parser()
    args = parser.parse_args()

    if args.only_haproxy:
        log(f"[!] Ignoring all other options as --only-haproxy was specified")
        update_haproxy()
        sys.exit(0)

    if args.deploy_no_create_fw and not args.deploy:
        log(f"[!] Ignoring option --deploy-no-create-fw as --deploy was not specified")
    if args.undeploy_delete_fw and not args.undeploy:
        log(f"[!] Ignoring option --undeploy-delete-fw as --undeploy was not specified")
    if args.create_fw and args.delete_fw:
        log(f"[-] Can only specify one of --create-fw and --delete-fw")
        sys.exit(1)
    if args.enable_fw and args.disable_fw:
        log(f"[-] Can only specify one of --enable-fw and --disable-fw")
        sys.exit(1)
    if args.wave and args.not_wave:
        log(f"[-] Can only specify one of --wave and --not-wave")
        sys.exit(1)

    if args.all:
        log(f"[*] Loading all challenges")
        chalpaths = get_chalpaths()
    elif args.wave:
        log(f"[*] Loading challenges of wave {args.wave}")
        chalpaths = get_chalpaths(wave=args.wave)
    elif args.not_wave:
        log(f"[*] Loading challenges not of wave {args.not_wave}")
        chalpaths = get_chalpaths(wave=args.not_wave, reverse=True)
    elif len(args.challenges) > 0:
        chalpaths = args.challenges
    else:
        log(f"[-] No challenge(s) specified, --wave not specified or --all not specified")
        sys.exit(1)

    if args.only_build:
        log(f"[!] Ignoring all other options as --only-build was specified")
        for chalpath in chalpaths:
            build_image(chalpath)
        sys.exit(0)

    if args.only_ctfcli_untrack:
        log(f"[!] Ignoring all other options as --only-ctfcli-untrack was specified")
        if args.all:
            ctfcli_untrack_all()
        else:
            for chalpath in chalpaths:
                ctfcli_untrack(chalpath)
        sys.exit(0)

    if args.only_push_ctfd:
        log(f"[!] Ignoring all other options as --only-push-ctfd was specified")
        for chalpath in chalpaths:
            ctfcli_push(chalpath, update=True)
        sys.exit(0)

    if args.state:
        log(f"[!] Ignoring all other options as --state was specified")
        for chalpath in chalpaths:
            ctfcli_chstate(chalpath, args.state)
        sys.exit(0)

    fw_action = None
    if args.create_fw:
        log(f"[!] Ignoring all other options as --create-fw was specified")
        fw_action = create_fw
    elif args.delete_fw:
        log(f"[!] Ignoring all other options as --delete-fw was specified")
        fw_action = delete_fw
    elif args.enable_fw:
        log(f"[!] Ignoring all other options as --enable-fw was specified")
        fw_action = enable_fw
    elif args.disable_fw:
        log(f"[!] Ignoring all other options as --disable-fw was specified")
        fw_action = disable_fw

    if fw_action is not None:
        for chalpath in chalpaths:
            fw_action(chalpath)
        sys.exit(0)

    build = not args.no_build
    deploy = args.deploy
    undeploy = args.undeploy
    createfw = not args.deploy_no_create_fw
    deletefw = args.undeploy_delete_fw
    push_ctfd = not args.no_push_ctfd

    if args.undeploy:
        undeploy_chals(chalpaths, deletefw)
    else:
        deploy_chals(chalpaths, build, deploy, createfw, push_ctfd)
    update_haproxy()
