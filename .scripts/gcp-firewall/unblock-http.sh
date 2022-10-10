#!/bin/sh

RULE_NAME="allow-http-haproxy"

gcloud compute firewall-rules update "${RULE_NAME}" --no-disabled
