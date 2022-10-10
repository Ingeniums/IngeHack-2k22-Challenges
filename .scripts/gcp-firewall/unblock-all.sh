#!/bin/sh

RULE_NAME="deny-challenges"

gcloud compute firewall-rules update "${RULE_NAME}" --disabled
