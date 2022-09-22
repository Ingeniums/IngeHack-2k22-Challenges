#!/bin/sh

PORT=9003

socat -dd -T300 tcp-l:$PORT,reuseaddr,fork,keepalive exec:/home/game/chall,stderr