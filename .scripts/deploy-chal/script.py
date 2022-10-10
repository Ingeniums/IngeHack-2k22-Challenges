#!/usr/bin/env python3

import argparse
import jinja2
from os import path
from config import *

SCRIPT_ROOT = path.dirname(__file__)
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(path.join(SCRIPT_ROOT, TEMPLATES_DIR)))

def argument_parser():
    parser = argparse.ArgumentParser(description="Generate deployment.yml and optionally service.yml of a challenge")

    parser.add_argument("--name", required=True, help="Challenge name")
    parser.add_argument("--category", required=True, help="Challenge category")
    parser.add_argument("--type", required=True, choices=["http", "tcp"], help="Challenge type (http or tcp)")
    parser.add_argument("--replicas", default=DEFAULT_REPLICAS, help="Number of pod replicas")
    parser.add_argument("--docker-registry", default=DOCKER_REGISTRY_BASE_LINK, help="Docker registry link")
    parser.add_argument("--docker-registry-challenge-name", help="Docker registry challenge name")
    parser.add_argument("--cpu-limit", type=int, default=CPU_LIMIT, help="Container CPU limit")
    parser.add_argument("--memory-limit", type=int, default=MEMORY_LIMIT, help="Container memory limit")
    parser.add_argument("--cpu-request", type=int, default=CPU_REQUEST, help="Container CPU request")
    parser.add_argument("--memory-request", type=int, default=MEMORY_REQUEST, help="Container memory request")
    parser.add_argument("--container-port", type=int, help="Container port")
    parser.add_argument("--initial-delay-seconds", type=int, default=INITIAL_DELAY_SECONDS, help="Number of initial delay seconds before starting the liveness probe")
    parser.add_argument("--period-seconds", type=int, default=PERIOD_SECONDS, help="Period in seconds before of the liveness probe")
    parser.add_argument("--node-port", type=int, help="Node port")

    return parser

def generate_file(filename):
    if path.exists(filename):
        raise Exception(f"'{filename}' already exists")
    else:
        template = JINJA_ENV.get_template(f"{filename}.j2")
        content = template.render(challenge=challenge)
        with open(filename, 'w') as f:
            f.write(content)

if __name__ == "__main__":
    parser = argument_parser()
    args = parser.parse_args()

    challenge = {
        "name": args.name,
        "category": args.category,
        "type": args.type,
        "replicas": args.replicas,
        "docker_registry": args.docker_registry,
        "docker_registry_challenge_name": args.docker_registry_challenge_name if args.docker_registry_challenge_name else args.name,
        "cpu_limit": args.cpu_limit,
        "memory_limit": args.memory_limit,
        "cpu_request": args.cpu_request,
        "memory_request": args.memory_request,
        "container_port": args.container_port,
        "initial_delay_seconds": args.initial_delay_seconds,
        "period_seconds": args.period_seconds,
        "node_port": args.node_port,
    }

    generate_file(DEPLOYMENT_FILE)

    if challenge['container_port'] is not None and challenge['node_port'] is not None:
        generate_file(SERVICE_FILE)
