#!/bin/sh

PORT=9001

socat -dd -T300 tcp-l:$PORT,reuseaddr,fork,keepalive exec:/home/game/chall,stderr
