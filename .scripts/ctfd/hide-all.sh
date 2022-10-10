#!/bin/sh

ALL_CHALLS_SCRIPT="all-challs.sh"
STATE_SCRIPT="state.sh"
DIRNAME="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ;pwd -P)"

for chal in $("${DIRNAME}/${ALL_CHALLS_SCRIPT}");do
  "${DIRNAME}/${STATE_SCRIPT}" "${chal}" hidden
done
