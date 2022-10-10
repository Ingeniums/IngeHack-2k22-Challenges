#!/bin/sh

if [ "${1}" = "-d" -o "${1}" = "--deploy" ]; then
  DEPLOY=true
  shift
fi

for chal in "$@"; do
  ctf challenge sync "$chal"
  if [ "$DEPLOY" = true ] && [ -f "${chal}/docker-compose.yml" ]; then
    cd "$chal"
    docker-compose build
    docker-compose push
    cd -
  fi
done

git add . && git commit . && git push
