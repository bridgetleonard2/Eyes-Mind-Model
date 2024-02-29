# Reading the Mind in the Eyes Test (RMET) Analysis with AI

## Introduction

This project explores the capabilities of AI models, specifically GPT-4 Vision API and LLava, in performing the Reading the Mind in the Eyes Test (RMET). RMET is a widely used tool in cognitive psychology, which assesses the ability to understand emotions by looking at a picture of eyes and selecting the emotion that best describes them from four options.

<div align="center">
  <img src="/task_materials/regular/01-playful-comforting-irritated-bored-300x175.jpg" alt="Sample RMET Image"/>
  <br>
  <i>Sample RMET Image with Options: [playful, comforting, irritated, bored]</i>
  <br>
</div>

Our research focuses on comparing the performance of GPT-4 Vision API and LLava in this context and improving LLava's performance through fine-tuning.

## Project Description

The RMET presents a significant challenge in understanding human emotions, a task typically thought to be exclusive to human cognitive abilities. This project aims to:

1. Assess the performance of GPT-4 Vision API and LLava on the RMET.
2. Identify the impact of training dataset size on the model's performance.
3. Fine-tune the LLava model using image-caption pairs related to various emotions.
4. Evaluate the improvement in LLava's performance post fine-tuning.

Through this project, we observed a **% increase in performance in the LLava model, post fine-tuning on a dataset of *n-size*.

## Results
### Fine-Tuning
We fine tuned the model on a dataset created using image caption pairs from Adobe Firefly and GPT-4 vision. We trained 4 different instances using different numbers of epochs:
<div align="center">
  <br>
  <img src="/llava_hyak/output/trainloss.png" width="450" alt="Training Loss over Epochs"/>
  <img src="/llava_hyak/output/evalloss.png" width="450" alt="Evaluation Loss over Epochs"/>
</div>

## Acknowledgements
Baron-Cohen, S., Jolliffe, T., Mortimore, C., & Robertson, M. (1997). Another advanced test of theory of mind: evidence from very high functioning adults with autism or asperger syndrome. Journal of child psychology and psychiatry, and allied disciplines, 38(7), 813–822. https://doi.org/10.1111/j.1469-7610.1997.tb01599.x
