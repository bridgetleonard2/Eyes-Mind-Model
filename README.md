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

Through this project, we observed a **% increase in performance in the LLava model, post fine-tuning on a 84 KB dataset (77 items).

## Results
### GPT-4v vs LLaVA
<div align="center">
  <br>
  <img src="/llava_hyak/output/gpt_llava_dist_overlay.png" width="800" alt="GPT-4v vs LLaVA performance on the RMET"/>
</div>

Density plots of GPT-4v and LLaVA performance overlayed on a human performance distribution. GPT-4v excels at the task, matching the higher ends of human performance while LLaVA barely meets the bottom-end of human performance.

### Fine-Tuning on Adobe Firefly-generated Images and GPT-4-generated captions
#### Fine-Tuning
To try to bridge the gap between GPT-4v and LLaVA performance, we fine-tuned the LLaVA on a dataset created using image caption pairs from Adobe Firefly and GPT-4 vision. We trained 4 different instances using different numbers of epochs:
<div align="center">
  <br>
  <img src="/llava_hyak/output/trainloss.png" width="500" alt="Training Loss over Epochs"/>
  <img src="/llava_hyak/output/evalloss.png" width="500" alt="Evaluation Loss over Epochs"/>
</div>

#### RMET Performance
We saw an increase in the performance of the fine-tuned models on the RMET task. Specifically, the models trained with 5 and 7 epochs saw a 12% increase in performance on the task.
<div align="center">
  <br>
  <img src="/llava_hyak/output/ft_performance.png" width="500" alt="Increase in performance over epochs"/>
</div>

<br>
The performance of the 5 and 7 epoch fine-tuned models often met the lower threshold of average human performance, and approached the performance of GPT-4v compared to the base model. 
<div align="center">
  <br>
  <img src="/llava_hyak/output/finetune_dist_overlay.png" width="800" alt="Comparing model performance"/>
</div>

##### Doubling the training data
We attempted to further increase LLaVA performance by providing double the training data for fine-tuning. We saw another boost of the 7-epoch model in performance. After fine-tuning, the best fine-tuned LLaVA model can now meet the lower end of average human performance.
<div align="center">
  <br>
  <img src="/llava_hyak/output/finetune_double_dist_overlay.png" width="800" alt="Comparing model performance"/>
</div>

## Conclusions
Current multi-modal models can meet human standards on emotion detections tasks. Specifically, GPT-4v meets the higher end of human performance while smaller models like LLaVA-1.5-13B reflect the lower end of human performance. This difference in model performance can likely be attributed to 1) different model architecture or 2) varying amounts of training data, or perhaps a combination of both.
To investigate if the performance difference is due to quantity of training data, we fine-tuned LLaVA with task-relevant data generated with Adobe Firefly (images) and GPT-4v (captions). We found that fine-tuning the LLaVA with 7 epochs significantly increase the model performance to meet the lower-average range of human performance. Although larger training datasets for fine-tuning may continue to increase LLaVA performance, it seems that some of GPT-4v's superior performance can likely be attributed to its larger, more complex, and widely unknown architecture.

## Acknowledgements
### LLaVA
[LLaVA GitHub](https://github.com/haotian-liu/LLaVA/tree/main)

- Haotian Liu, Chunyuan Li, Yuheng Li, Bo Li, Yuanhan Zhang, Sheng Shen, and Yong Jae Lee. (2024). LLaVA-NeXT: Improved reasoning, OCR, and world knowledge. [Link](https://llava-vl.github.io/blog/2024-01-30-llava-next/).

- Haotian Liu, Chunyuan Li, Yuheng Li, and Yong Jae Lee. (2023). Improved Baselines with Visual Instruction Tuning. arXiv:2310.03744.

- Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae Lee. (2023). Visual Instruction Tuning. NeurIPS.

### RMET
Baron-Cohen, S., Jolliffe, T., Mortimore, C., & Robertson, M. (1997). Another advanced test of theory of mind: evidence from very high functioning adults with autism or asperger syndrome. Journal of child psychology and psychiatry, and allied disciplines, 38(7), 813–822. https://doi.org/10.1111/j.1469-7610.1997.tb01599.x
