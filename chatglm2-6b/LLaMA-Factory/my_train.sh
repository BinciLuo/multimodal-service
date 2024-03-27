CUDA_VISIBLE_DEVICES=0 python3 src/train_bash.py \
    --stage sft \
    --do_train \
    --model_name_or_path /home/user/netdisk/data/chatglm2-6b \
    --dataset chat_dataset \
    --template default \
    --finetuning_type lora \
    --lora_target all \
    --output_dir loras \
    --overwrite_cache \
    --per_device_train_batch_size 4 \
    --gradient_accumulation_steps 4 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --save_steps 100 \
    --learning_rate 5e-5 \
    --num_train_epochs 3.0 \
    --plot_loss \
    --fp16

CUDA_VISIBLE_DEVICES=0 python3 src/web_demo.py \
    --model_name_or_path /home/user/netdisk/data/chatglm2-6b \
    --adapter_name_or_path loras/checkpoint-300 \
    --template default \
    --finetuning_type lora

CUDA_VISIBLE_DEVICES=0 API_PORT=27777 python3 src/api_demo.py \
    --model_name_or_path /home/user/netdisk/data/chatglm2-6b \
    --adapter_name_or_path loras/checkpoint-300 \
    --template default \
    --finetuning_type lora
