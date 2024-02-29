#!/bin/bash

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
    echo "Question ${i}: ${questions[i]}, Image file: ${image_files[i]}"
    prompt="Choose which word best describes what the person in the picture is thinking or feeling based on just their eyes alone. You may feel that more than one word is applicable, but please choose just one word, the word which you consider to be most suitable. Your 4 choices are: ${questions[i]}"
    echo "$prompt"

    image_path="$directory/${image_files[i]}"
    echo "$image_path"

    apptainer run \
    --bind llava_hyak/output:/container/output \
    --bind llava_hyak/rmet_materials:/container/rmet_materials \
    oras://ghcr.io/uw-psych/llava-container/llava-container:latest \
    llava-run \
    --model-path liuhaotian/llava-v1.5-13b \
    --query "$prompt" \
    --image-file "$image_path" \
    | tail -n 1 \
    | tee -a llava_hyak/rmet_results/rmet_base-2.txt # "tee" writes the output to output.json while also printing it on the screen
done
