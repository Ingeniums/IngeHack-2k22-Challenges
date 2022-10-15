#!/bin/sh

PORT=9006

socat -dd -T300 tcp-l:$PORT,reuseaddr,fork,keepalive exec:/home/game_2/chall,stderr