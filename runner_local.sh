#!/bin/bash
# Kill process before
kill -TERM $(ps aux | grep 'middleware' | awk '{print $2}')
kill -TERM $(ps aux | grep 'webui.py' | awk '{print $2}')

# Change directory to middleware
cd middleware

# Run Middleware
bash docker.sh &

# Change directory to gradio_web
cd ../gradio_web

# Run Gradio
export SEG_MODEL_ENV='local'
bash docker.sh
