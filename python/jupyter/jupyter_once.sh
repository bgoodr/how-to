#!/bin/bash

# Launch a single instance of a jupyter process to avoid spawning
# multiple Linux processes (each process can have multiple "kernels").
# Without this, just directly executing "jupyter notebook" will spawn
# multiple servers numbered off at http://localhost:8888/,
# http://localhost:8889/ ...

if [ "$1" = "-k" ]
then
  echo "Note: Killing all jupyter servers."
  kill $(pgrep jupyter)
  exit
fi

if ! which jupyter
then
  echo 'ERROR: You need to install jupyter using "conda install jupyter" first'
  exit 1
fi

url=$(jupyter notebook list | grep -v 'Currently' | sort | head -1 | sed 's% :: .*$%%g')

if [ -n "$url" ]
then
  echo "Note: Existing server running, not starting a new server."
  # https://stackoverflow.com/a/36477085
  python -m webbrowser "$url"
else
  echo "Note: No existing jupyter server running, starting a brand new one."
  nohup jupyter notebook 2>&1 &
  # Wait for a bit for it to start so as to avoid killing it:
  sleep 5
fi
