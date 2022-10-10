#!/bin/sh

RULE_NAME="deny-docker-challenges"

gcloud compute firewall-rules update "${RULE_NAME}" --disabled
