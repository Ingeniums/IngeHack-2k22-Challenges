#!/bin/sh

DEPLOY_DIR="deploy"
ALL_CHALLS_SCRIPT="../ctfd/all-challs.sh"
DIRNAME="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ;pwd -P)"

for chal in $("${DIRNAME}/${ALL_CHALLS_SCRIPT}");do
  if [ -d "${chal}/${DEPLOY_DIR}" ]; then
    kubectl apply -f "${chal}/${DEPLOY_DIR}"
  fi
done
