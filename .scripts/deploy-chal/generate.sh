#!/bin/sh

DEPLOY_DIR="deploy"
SCRIPTNAME="script.py"
DIRNAME="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ;pwd -P)"

mkdir -p "$DEPLOY_DIR" && cd "$DEPLOY_DIR"

"${DIRNAME}/${SCRIPTNAME}" "$@"
