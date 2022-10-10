#!/bin/sh

RULE_NAME="deny-ctfd"

gcloud compute firewall-rules update "${RULE_NAME}" --no-disabled
