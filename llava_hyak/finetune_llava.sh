#!/bin/bash

apptainer run --nv \
    --bind llava_hyak/train:/container/training_script \
    --bind llava_hyak/adobe_dataset_full:/container/dataset \
    --bind llava_hyak/output:/container/output \
    --bind llava_hyak/scripts:/container/scripts \
    oras://ghcr.io/uw-psych/llava-container/llava-container-train:latest \
    deepspeed /container/training_script/train_mem.py \
    --lora_enable True \
    --lora_r 128 \
    --lora_alpha 256 \
    --mm_projector_lr 2e-5 \
    --deepspeed /container/scripts/zero3.json \
    --model_name_or_path liuhaotian/llava-v1.5-13b \
    --version v1 \
    --data_path /container/dataset/train/train_data.json \
    --validation_data_path /container/dataset/validation/val_data.json \
    --image_folder /container/dataset/images \
    --vision_tower openai/clip-vit-large-patch14-336 \
    --mm_projector_type mlp2x_gelu \
    --mm_vision_select_layer -2 \
    --mm_use_im_start_end False \
    --mm_use_im_patch_token False \
    --image_aspect_ratio pad \
    --group_by_modality_length True \
    --bf16 True \
    --output_dir /container/output/checkpoints/llava-v1.5-13b-task-lora-fullAdobe \
    --num_train_epochs 5 \
    --per_device_train_batch_size 16 \
    --per_device_eval_batch_size 4 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "epoch" \
    --save_strategy "steps" \
    --save_steps 50000 \
    --save_total_limit 1 \
    --learning_rate 2e-4 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --dataloader_num_workers 4 \
    --lazy_preprocess True \
    --report_to wandb
