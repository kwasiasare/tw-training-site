---
course: ml-engineer
title: Fine-Tuning with LoRA and PEFT
month: 5
monthTitle: 'LLM Engineering: Transformers, RAG, and Fine-Tuning'
lesson: 4
summary: Learn when fine-tuning beats prompting or RAG, and how parameter-efficient fine-tuning (PEFT)
  makes adapting large models practical. You will implement LoRA with the Hugging Face peft library, understand
  QLoRA for fitting big models on a single GPU, and apply a decision framework before building a small
  fine-tuning mini-project.
objectives:
- Decide when fine-tuning is warranted versus prompting or retrieval-augmented generation
- Explain why full fine-tuning of large models is costly in memory and compute
- Describe how LoRA freezes base weights and trains low-rank adapter matrices (delta-W = BA)
- Implement LoRA on a Hugging Face model using LoraConfig and get_peft_model
- Explain how QLoRA combines 4-bit quantization with LoRA to fit large models on one GPU
- Apply a prompt-vs-RAG-vs-fine-tune decision framework and evaluate a fine-tuned model against a baseline
video: mle-m5-l04-fine-tuning-with-lora-and-peft.mp4
quiz:
- q: When is fine-tuning the right tool rather than prompting or RAG?
  options:
  - Fine-tuning is always cheaper and should be the default choice
  - Whenever the knowledge base changes every few minutes
  - When you need to bake consistent task or domain-specific behavior into the model's weights and prompting
    or RAG fall short
  - Only when the pretrained model cannot perform inference at all
  answer: 2
  why: Fine-tuning updates the weights to internalize a style, format, or domain skill. It shines when
    prompting and RAG cannot reliably produce the desired behavior, but it is not always the cheapest
    option.
- q: What does LoRA actually train?
  options:
  - It freezes the base weights and trains small low-rank adapter matrices A and B
  - It retrains every weight in the network at full precision
  - It removes layers from the model to save memory
  - It only fine-tunes the tokenizer vocabulary
  answer: 0
  why: LoRA keeps the large pretrained weights frozen and injects trainable low-rank matrices, so only
    a tiny fraction of parameters are updated and saved.
- q: In LoRA, how is the update to a weight matrix expressed?
  options:
  - delta-W = W squared
  - delta-W = softmax(W)
  - delta-W = W + b, a learned bias term
  - delta-W = B times A, the product of two low-rank matrices
  answer: 3
  why: LoRA approximates the weight update as the product of two low-rank matrices B and A, which together
    have far fewer parameters than the full matrix they adapt.
- q: What is the key idea behind QLoRA?
  options:
  - It trains the entire model in 64-bit precision for maximum accuracy
  - It quantizes the frozen base model to 4-bit and trains LoRA adapters on top, fitting large models
    on a single GPU
  - It eliminates the need for any GPU during training
  - It converts the model to ONNX before training
  answer: 1
  why: QLoRA loads the frozen base model in 4-bit precision to slash memory use, then trains small LoRA
    adapters in higher precision on top, enabling fine-tuning of very large models on one GPU.
- q: You need the model to answer questions about a frequently changing internal knowledge base. Which
    approach is usually the best first choice?
  options:
  - Full fine-tuning the model every night
  - LoRA fine-tuning the model every hour
  - Retrieval-augmented generation (RAG) over the knowledge base
  - 4-bit quantization of the base model alone
  answer: 2
  why: When information changes often and must stay current, RAG retrieves up-to-date documents at query
    time without retraining, making it cheaper and fresher than repeatedly fine-tuning.
- q: Name one practical reason you might prefer LoRA fine-tuning over full fine-tuning.
  answer: 'Far fewer trainable parameters, so it needs much less GPU memory and produces small adapter
    files (also acceptable: faster training, easy to swap adapters, base model stays shared)'
  why: Because LoRA freezes the base weights and trains only small low-rank adapters, it dramatically
    reduces memory and storage while letting you keep one shared base model and swap adapters per task.
resources:
- label: Hugging Face PEFT Documentation
  url: https://huggingface.co/docs/peft/index
- label: 'LoRA: Low-Rank Adaptation of Large Language Models (arXiv)'
  url: https://arxiv.org/abs/2106.09685
- label: Hugging Face Transformers Trainer Documentation
  url: https://huggingface.co/docs/transformers/main_classes/trainer
- label: 'QLoRA: Efficient Finetuning of Quantized LLMs (arXiv)'
  url: https://arxiv.org/abs/2305.14314
---

## Why Fine-Tune?

A pretrained model already knows a great deal, but it may not behave exactly the way your task needs. **Fine-tuning** continues training on your own labeled data so the model internalizes a specific style, output format, or domain skill. Reach for it when you need consistent behavior that prompting cannot reliably produce, or when you want the model to learn a task (e.g. classifying support tickets) rather than just retrieve facts.

Fine-tuning is **not** always the answer. Prompting is free to iterate on, and RAG is usually better when answers depend on up-to-date or proprietary documents. Always ask whether a cheaper option is good enough first.

## Full Fine-Tuning vs PEFT

**Full fine-tuning** updates every weight in the model. For a model with billions of parameters this is brutal: you must store gradients and optimizer states for every parameter, often needing many times the model's size in GPU memory. You also end up with a full-size copy of the model for each task.

**Parameter-efficient fine-tuning (PEFT)** sidesteps this by freezing the pretrained weights and training only a small number of new parameters. You get most of the quality of full fine-tuning at a fraction of the memory and storage cost, and a single base model can be shared across many tasks.

## LoRA: Low-Rank Adaptation

LoRA is the most popular PEFT method. The insight: the *change* a task makes to a big weight matrix W can be approximated by a **low-rank** update. Instead of learning a full update matrix, LoRA learns two small matrices A and B and expresses the update as delta-W = B A. The base W stays frozen; only A and B are trained.

Because A and B are low rank (controlled by `r`), the trainable parameters are tiny, often well under 1% of the model. Only the adapters are saved, so checkpoints are megabytes, not gigabytes.

## Implementing LoRA with PEFT

The Hugging Face `peft` library wraps any `transformers` model in a few lines.

```python
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForSequenceClassification

base = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=2
)
config = LoraConfig(
    r=8, lora_alpha=16, lora_dropout=0.05,
    target_modules=["q_lin", "v_lin"],
)
model = get_peft_model(base, config)
model.print_trainable_parameters()  # tiny % of params are trainable
```

`r` sets the adapter rank, `lora_alpha` scales the update, and `target_modules` picks which layers to adapt (here the query and value projections). You then train `model` with the normal `transformers` `Trainer`.

## QLoRA: Fitting Big Models on One GPU

LoRA shrinks the *trainable* parameters, but the frozen base still occupies memory. **QLoRA** adds 4-bit quantization of the frozen base so even a large model fits on a single GPU, while LoRA adapters train in higher precision on top.

```python
from transformers import BitsAndBytesConfig, AutoModelForCausalLM
from peft import prepare_model_for_kbit_training

bnb = BitsAndBytesConfig(load_in_4bit=True)
base = AutoModelForCausalLM.from_pretrained(
    "some-base-model", quantization_config=bnb
)
base = prepare_model_for_kbit_training(base)
# then wrap with get_peft_model(base, lora_config) as before
```

`prepare_model_for_kbit_training` readies the quantized model for stable adapter training, so large-model fine-tuning can run on one consumer-class GPU.

## Prompt vs RAG vs Fine-Tune: A Decision Framework

Pick the lightest tool that solves the problem:

- **Prompting / few-shot**: fastest to try, no training, no data pipeline. Best for general tasks and quick iteration.
- **RAG**: when answers depend on changing or proprietary facts. Keeps knowledge fresh without retraining; you update documents, not weights.
- **Fine-tuning (LoRA/QLoRA)**: when you need a consistent behavior, format, or specialized skill baked into the model, and you have a few hundred-plus labeled examples.

These combine: you can fine-tune for *behavior* and still use RAG for *facts*. Start cheap, measure, and only escalate when the simpler option provably underperforms.

## Mini-Project Brief

**Goal:** Fine-tune a small pretrained model on a domain text-classification dataset with LoRA, and prove it beats a no-training baseline.

**Steps:**
1. Pick a labeled text-classification dataset (e.g. a sentiment or topic dataset from the Hub).
2. Establish a **baseline**: a zero-shot or few-shot prompt with a base model, and record its accuracy/F1.
3. Wrap `distilbert-base-uncased` (or similar) with `LoraConfig` + `get_peft_model` and train with the `Trainer`.
4. Call `print_trainable_parameters()` and record the trainable-parameter count and percentage.
5. Evaluate the fine-tuned model on the held-out test set and compare to the baseline.

**Deliverables:**
- A training script/notebook that runs end to end.
- The saved LoRA adapter directory (not a full model copy).
- A short report: dataset, baseline metric, fine-tuned metric, trainable-param count and percent, and a one-paragraph reflection on whether fine-tuning was worth it versus prompting or RAG.

## Key Takeaways

Fine-tuning adapts a model's weights, but it is one option among prompting and RAG, not the default. LoRA freezes the base and trains low-rank adapters (delta-W = BA), saving only tiny adapter files. QLoRA adds 4-bit quantization to fit big models on one GPU. Choose the lightest approach that meets your quality bar, and always measure against a baseline.
