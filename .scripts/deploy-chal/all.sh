#!/bin/sh

DEPLOY_DIR="deploy"

# apply or delete
K8S_CMD="${1}"

for dir in $(find -name "${DEPLOY_DIR}" -type d); do
  kubectl "${K8S_CMD}" -f "${dir}"
done
