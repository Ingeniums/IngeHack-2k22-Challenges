#!/bin/bash

PREFIX="CyberErudites"

LINES="$(grep -Proh "[^\^]\K${PREFIX}\{.*?\}" | wc -l)"
(( LINES > 1 )) || { echo "Flag not found or found only once" >&2; grep -Pr "[^\^]\K${PREFIX}\{.*?\}" >&2; exit 1; }

UNIQUE="$(grep -Proh "[^\^]\K${PREFIX}\{.*?\}" | sort -u | wc -l)"
(( UNIQUE > 1 )) && { echo "Found non matching flags" >&2; grep -Pr "[^\^]\K${PREFIX}\{.*?\}" >&2; exit 1; }

FLAG="$(grep -Proh "[^\^]\K${PREFIX}\{.*?\}" | sort -u)"

echo "Flag '${FLAG}' is unique!"
