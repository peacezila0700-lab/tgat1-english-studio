#!/bin/sh
# usage: serve.sh DIR PORT
cd "$1" && exec python3 -m http.server "$2" --bind 127.0.0.1
