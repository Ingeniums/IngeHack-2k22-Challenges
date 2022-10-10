#!/bin/bash

CHALLENGE="${1}"

[ -d "${CHALLENGE}" ] || { echo "No such challenge: '${CHALLENGE}'" >&2; exit 1; }

RULE_NAME="allow-${CHALLENGE/\//-}"
echo "Enabling firewall rule : '${RULE_NAME}'"

gcloud compute firewall-rules update "${RULE_NAME}" --no-disabled
