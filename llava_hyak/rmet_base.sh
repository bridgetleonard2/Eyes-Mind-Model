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
    oras://ghcr.io/uw-psych/llava-container/llava-container-train:latest \
    llava-run \
    --model-path liuhaotian/llava-v1.5-13b \
    --query "$prompt" \
    --image-file "$image_path" \
    | tail -n 1 \
    | tee -a llava_hyak/rmet_results/rmet_base-1.txt # "tee" writes the output to output.json while also printing it on the screen
done

# Report number correct
answers=()

while IFS= read -r line; do
  answers+=("$line")
done < "llava_hyak/rmet_materials/answers.txt"

results=()

while IFS= read -r line; do
  results+=("$line")
done < "rmet_results/rmet_base-1.txt"

# Get the length of the arrays
length=${#results[@]}

counter=0

# Loop through each index of the arrays
for ((i=0; i<length; i++)); do
    # Convert both elements to lowercase
    elem1="${results[i],,}"
    elem2="${answers[i],,}"

    # Compare the elements
    if [ "$elem1" == "$elem2" ]; then
        ((counter+=1))
    fi
done

echo $counter