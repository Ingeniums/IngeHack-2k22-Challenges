#!/bin/sh

if [ $# = 0 ]; then
  git add . && git commit && git push
else
  git add "$@" && git commit "$@" && git push
fi
