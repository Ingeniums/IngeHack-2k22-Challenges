#!/bin/sh

CHALS_JSON="config/chals.json"
PRIORITY="950"
TCP_TYPE="tcp"
SOURCE_RANGES="0.0.0.0/0"
TARGET_TAGS="haproxy"
RULE_NAME="deny-challenges"
RULES="tcp:1100-1899,tcp:80"

gcloud compute firewall-rules create "${RULE_NAME}" --direction=INGRESS --priority="${PRIORITY}" --network=default --action=DENY --rules="${RULES}" --source-ranges="${SOURCE_RANGES}" --target-tags="${TARGET_TAGS}"
