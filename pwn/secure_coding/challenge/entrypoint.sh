#!/bin/sh

PORT=9002
socat -dd -T300 tcp-l:$PORT,reuseaddr,fork,keepalive exec:/home/coding/chall,stderr