#!/bin/sh

CHALS_JSON="config/chals.json"
PRIORITY="1000"
TCP_TYPE="tcp"
SOURCE_RANGES="0.0.0.0/0"
TARGET_TAGS="haproxy"

for chal in $(jq -c ".[]" "${CHALS_JSON}"); do
  name="$(echo "$chal" | jq -r ".name")"
  category="$(echo "$chal" | jq -r ".category")"
  port="$(echo "$chal" | jq -r ".port")"
  type="$(echo "$chal" | jq -r ".type")"

  rule="allow-${category}-${name}"

  if [ "${type}" = "${TCP_TYPE}" ] && ! gcloud compute firewall-rules describe "${rule}" >/dev/null 2>&1; then
    gcloud compute firewall-rules create "${rule}" --direction=INGRESS --priority="${PRIORITY}" --network=default --action=ALLOW --rules=tcp:"${port}" --source-ranges="${SOURCE_RANGES}" --target-tags="${TARGET_TAGS}"
  fi
done
