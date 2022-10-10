#!/bin/bash

CHALLENGES_FILE="challenges.txt"
DEPTH="3"

if [ -f "${CHALLENGES_FILE}" ]; then
  cat "${CHALLENGES_FILE}"
else
  for c in $(find -mindepth "${DEPTH}" -maxdepth "${DEPTH}" -name challenge.yml); do
    c="${c%/challenge.yml}"
    echo "${c#./}"
  done
fi
