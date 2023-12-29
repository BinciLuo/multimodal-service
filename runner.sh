#!/bin/bash
# Kill process before
kill -TERM $(ps aux | grep 'middleware' | awk '{print $2}')
kill -TERM $(ps aux | grep 'webui.py' | awk '{print $2}')

# Change directory to middleware
cd middleware

# Run local_middleware.sh in the background
bash local_middleware.sh &

# Change directory to gradio_web
cd ../gradio_web

# Run local_gradio.sh
bash docker.sh &
