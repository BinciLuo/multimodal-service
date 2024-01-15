echo "You're running webui with env_variables: MIDDLEWARE_ENV:${MIDDLEWARE_ENV}, GR_PORT:${GR_PORT}"
export MIDDLEWARE_ENV=local
export GR_PORT=80
python3 -u webui.py