cd /app/stable-diffusion-webui/
git apply /home/user/netdisk/data/lora_api_and_cache.patch
cd ..
bash start.sh --api --skip-prepare-environment --no-hashing