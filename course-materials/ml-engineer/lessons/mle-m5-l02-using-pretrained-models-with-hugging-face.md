---
course: ml-engineer
title: Using Pretrained Models with Hugging Face Transformers
month: 5
monthTitle: 'LLM Engineering: Transformers, RAG, and Fine-Tuning'
lesson: 2
summary: Learn to reuse state-of-the-art pretrained models instead of training from scratch, using the
  Hugging Face Hub and the transformers library. You will run fast inference with pipeline(), drop down
  to AutoTokenizer and AutoModel for full control, process batches across tasks, and apply practical techniques
  like GPU placement, torch.no_grad, and quantization to run large models efficiently.
objectives:
- Explain the pretrained-model paradigm and why transfer learning beats training from scratch
- Run inference quickly for common tasks using the transformers pipeline() helper
- Use AutoTokenizer and AutoModel classes for lower-level, customizable inference
- Process batches of text efficiently with padding, truncation, and return_tensors
- Apply device placement, torch.no_grad, batching, and quantization to run models efficiently
- Choose an appropriate model by task, size, and license, and decide between hosted APIs and self-hosting
video: mle-m5-l02-using-pretrained-models-with-hugging-face.mp4
quiz:
- q: What is the main advantage of using a pretrained model rather than training one from scratch?
  options:
  - It requires no data or compute under any circumstances
  - It always outperforms every possible custom-built model
  - It transfers knowledge learned on large corpora, saving data and compute
  - It eliminates the need for a tokenizer entirely
  answer: 2
  why: Pretrained models encode general language or vision knowledge learned on massive datasets, so reusing
    them via transfer learning gives strong results with far less data and compute than training from
    scratch.
- q: Which transformers helper gives the fastest path to inference for a standard task?
  options:
  - pipeline()
  - AutoConfig()
  - Trainer()
  - DataLoader()
  answer: 0
  why: pipeline() bundles the tokenizer, model, and post-processing into a single callable, so you can
    run a task like sentiment-analysis in one or two lines without manual setup.
- q: When tokenizing a batch of variable-length texts, which arguments produce uniform-length PyTorch
    tensors ready for the model?
  options:
  - shuffle=True, drop_last=True
  - device_map='auto'
  - load_in_4bit=True
  - padding=True, truncation=True, return_tensors='pt'
  answer: 3
  why: padding pads shorter sequences to a common length, truncation caps overly long ones, and return_tensors='pt'
    returns PyTorch tensors, giving a rectangular batch the model can consume.
- q: Why should inference be wrapped in torch.no_grad()?
  options:
  - It automatically moves the model to the GPU
  - It disables gradient tracking, saving memory and speeding up inference
  - It applies softmax to the model's logits
  - It downloads the model weights from the Hub
  answer: 1
  why: During inference you do not need gradients; torch.no_grad() stops autograd from building the computation
    graph, which reduces memory usage and runs faster.
- q: Which technique reduces a large model's memory footprint so it fits on a smaller GPU?
  options:
  - Increasing the batch size
  - Using a faster tokenizer
  - Quantization, such as 4-bit loading via bitsandbytes
  - Disabling truncation
  answer: 2
  why: Quantization stores weights at lower precision (for example 4-bit or 8-bit), dramatically cutting
    memory use so multi-billion-parameter models can run on consumer GPUs with minimal accuracy loss.
- q: In one word, what does AutoModelForSequenceClassification output that you pass to argmax to get the
    predicted class?
  answer: logits
  why: Classification models return raw, unnormalized scores called logits; taking the argmax over the
    logits selects the highest-scoring class without needing an explicit softmax.
resources:
- label: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
- label: 'Hugging Face Hub: Browse Models'
  url: https://huggingface.co/models
- label: Transformers Pipelines and Task Reference
  url: https://huggingface.co/docs/transformers/main_classes/pipelines
- label: Quantization Guide (bitsandbytes, 4-bit/8-bit)
  url: https://huggingface.co/docs/transformers/quantization/bitsandbytes
---

## Overview

Modern NLP rarely starts from a blank model. Instead you download a model that has already been trained on enormous text corpora and adapt it to your task. This lesson shows how to use the **Hugging Face Hub** and the **transformers** library to run pretrained models, from one-line inference to full low-level control, plus the practical tricks needed to run large models efficiently.

## 1. The Pretrained-Model Paradigm

Training a transformer from scratch costs millions of dollars and requires terabytes of text. The smarter approach is **transfer learning**: reuse a model whose weights already encode grammar, facts, and reasoning patterns, then apply it directly or fine-tune it on a small dataset.

The payoff is enormous: you get state-of-the-art results with a few lines of code, a modest GPU (or none), and little or no labeled data. The Hub hosts hundreds of thousands of these models, each identified by a name like `distilbert-base-uncased-finetuned-sst-2-english`.

## 2. The Hub and pipeline()

The fastest way to run a model is the `pipeline()` helper. It bundles the tokenizer, model, and post-processing into a single callable.

```python
from transformers import pipeline

clf = pipeline("sentiment-analysis")
print(clf("I love this course"))
# [{'label': 'POSITIVE', 'score': 0.99}]
```

If you do not name a model, the pipeline picks a sensible default for the task. You can also request a specific one with `pipeline("summarization", model="facebook/bart-large-cnn")`. Common task strings include `sentiment-analysis`, `text-classification`, `ner`, `summarization`, `translation`, and `text-generation`.

## 3. Lower-Level Control: AutoTokenizer + AutoModel

When you need control over batching, devices, or outputs, drop down to the `Auto` classes. The tokenizer converts text to token IDs; the model maps those IDs to outputs.

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

name = "distilbert-base-uncased-finetuned-sst-2-english"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(name)
```

The `AutoModelFor...` family selects the right architecture head for your task: `AutoModelForSequenceClassification`, `AutoModelForTokenClassification`, `AutoModelForCausalLM`, and `AutoModelForSeq2SeqLM` are the ones you will reach for most often.

## 4. Batch Inference Across Tasks

To classify several texts at once, tokenize them together with padding and truncation so they form a rectangular tensor, then run a forward pass.

```python
texts = ["great movie", "terrible plot"]
inputs = tok(texts, padding=True, truncation=True, return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
preds = logits.argmax(dim=-1)
labels = [model.config.id2label[i] for i in preds.tolist()]
print(labels)  # ['POSITIVE', 'NEGATIVE']
```

The same pattern adapts to other tasks: a NER pipeline tags entities per token, a summarizer returns generated text, and a classifier returns per-class scores. Batching many inputs in one call is far faster than looping one at a time.

## 5. Performance: Device, Batching, no_grad, and Quantization

Three habits make inference fast and memory-friendly:

- **Device placement.** Move the model and inputs to the GPU. For large models, let the library shard automatically with `from_pretrained(name, device_map="auto")`; otherwise call `model.to("cuda")` and `inputs.to("cuda")`.
- **Batching + no_grad.** Always wrap inference in `torch.no_grad()` so autograd does not build a graph, and group inputs into batches to maximize GPU utilization.
- **Quantization.** Billion-parameter models may not fit in GPU memory at full precision. Loading weights in 4-bit or 8-bit (via the `bitsandbytes` integration) shrinks memory use several-fold with minimal accuracy loss.

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

bnb = BitsAndBytesConfig(load_in_4bit=True)
llm = AutoModelForCausalLM.from_pretrained(
    "some-7b-model", quantization_config=bnb, device_map="auto")
```

## 6. Choosing a Model and Hosted vs Self-Hosted

Pick a model by matching three things: the **task** (does an appropriate `AutoModelFor...` head exist?), the **size** (can it fit your latency and memory budget?), and the **license** (is commercial use permitted?). Filter the Hub by task, library, and license to narrow the field, and prefer popular, well-documented checkpoints.

Finally, decide where it runs. A **hosted inference API** removes all infrastructure work and scales on demand, ideal for prototypes and bursty traffic. **Self-hosting** gives you data privacy, predictable cost at high volume, and offline control, at the price of managing GPUs. Many teams prototype on a hosted API, then self-host once usage and requirements are clear.

## Key Takeaways

Reuse, do not rebuild: pretrained models give you strong results cheaply. Reach for `pipeline()` first, drop to `AutoTokenizer` + `AutoModelFor...` when you need control, batch your inputs under `torch.no_grad()`, and use device placement and quantization to fit large models. Choose by task, size, and license, and pick hosted versus self-hosted to match your scale and privacy needs.
