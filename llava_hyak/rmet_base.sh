#!/bin/bash
# Start by clearing cache
rm -R .cache/huggingface

# Set up cache directories:
export APPTAINER_CACHEDIR="/gscratch/scrubbed/${USER}/.cache/apptainer"
export HUGGINGFACE_HUB_CACHE="/gscratch/scrubbed/${USER}/.cache/huggingface"
mkdir -p "${APPTAINER_CACHEDIR}" "${HUGGINGFACE_HUB_CACHE}"

# Set up Apptainer:
export APPTAINER_BIND=/gscratch APPTAINER_WRITABLE_TMPFS=1 APPTAINER_NV=1

# Define questions for the task
questions=()

# Read each line from the file and append to the array
while IFS= read -r line; do
  questions+=("$line")
done < "llava_hyak/rmet_materials/questions.txt"

# Define the images
directory="llava_hyak/rmet_materials/images"

image_files=()

# Loop through the files in the directory and add them to the array
for file in "$directory"/*; do
  image_files+=("$(basename "$file")")
done

# Assuming both arrays have the same length
for ((i = 0; i < ${#questions[@]}; i++)); do
    prompt="Choose which word best describes what the person in the picture is thinking or feeling based on just their eyes alone. You may feel that more than one word is applicable, but please choose just one word, the word which you consider to be most suitable. Your 4 choices are: ${questions[i]}"
    echo "$prompt"

    image_path="$directory/${image_files[i]}"
    echo "$image_path"

    output=$(apptainer run \
    --bind llava_hyak/rmet_materials:/container/rmet_materials \
    oras://ghcr.io/uw-psych/llava-container/llava-container-train:latest \
    llava-run \
    --model-path liuhaotian/llava-v1.5-13b \
    --query "$prompt" \
    --image-file "$image_path" 2>&1)
    
    # Print the entire output to the screen
    echo "$output"

    # Append only the last line of the output to the file
    echo "$output" | tail -n 1 | tee -a llava_hyak/rmet_results/rmet_base-2.txt # "tee" writes the output to output.json while also printing it on the screen
done
