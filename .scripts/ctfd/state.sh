#!/bin/bash

[ $# -lt 2 ] && { echo "Usage: $0 CHALLENGE STATE" >&2; exit 1; }

challenge="$1"
state="$2"

if [ "$state" != "hidden" -a "$state" != "visible" ]; then
  echo "Invalid state: \"$state\"" >&2
  echo "Valid states: hidden, visible" >&2
  exit 1
else
  case "$state" in
    hidden)
      other_state=visible
    ;;
    visible)
      other_state=hidden
    ;;
    *)
      echo "Invalid state: \"$state\"" >&2
      echo "Valid states: hidden, visible" >&2
      exit 1
  esac

  [ ! -d "${challenge}" -o ! -f "${challenge}/challenge.yml" ] && { echo "Cannot find challenge \"$challenge\"" >&2; exit 1; }

  sum="$(md5sum "${challenge}/challenge.yml")"
  sed -i "s/state: ${other_state}/state: ${state}/" "${challenge}/challenge.yml"
  if [ "$(md5sum "${challenge}/challenge.yml")" != "${sum}" ]; then
    ~/.local/bin/ctf challenge sync "${challenge}"
    echo "'${challenge}' is now ${state}"
  fi
fi
