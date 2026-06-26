---
course: ml-engineer
title: Transformers and the Attention Mechanism
month: 5
monthTitle: 'LLM Engineering: Transformers, RAG, and Fine-Tuning'
lesson: 1
summary: Understand the transformer architecture that powers every modern large language model. We trace
  text from raw characters through tokenization, embeddings, and positional encoding into the self-attention
  mechanism, then build up to multi-head attention, the encoder/decoder block, and how scaling these models
  turns transformers into LLMs.
objectives:
- Explain why transformers replaced RNNs for sequence modeling
- Convert text into tokens and integer IDs using subword (BPE) tokenization
- Describe how embeddings and positional encoding represent tokens and order
- Compute scaled dot-product self-attention from Q, K, and V matrices
- Diagram multi-head attention and the encoder/decoder block at a high level
- Connect the transformer architecture to how modern LLMs are pretrained and scaled
video: mle-m5-l01-transformers-and-the-attention-mechanism.mp4
quiz:
- q: What key advantage do transformers have over recurrent neural networks (RNNs) for processing sequences?
  options:
  - They require far less training data than RNNs
  - They are guaranteed to never overfit
  - They process all tokens in parallel and capture long-range dependencies directly
  - They eliminate the need for any matrix multiplication
  answer: 2
  why: RNNs process tokens sequentially, which is slow and tends to lose information across long distances.
    Transformers attend to all positions at once, enabling parallel computation and direct modeling of
    long-range dependencies.
- q: Why is subword (BPE-style) tokenization preferred over splitting text into whole words?
  options:
  - It handles rare and unseen words by composing them from smaller known pieces
  - It always produces exactly one token per sentence
  - It removes the need for an embedding layer
  - It guarantees every language uses the same vocabulary size
  answer: 0
  why: Subword tokenization keeps a fixed vocabulary while representing rare or novel words as sequences
    of known subword units, avoiding the out-of-vocabulary problem that plagues word-level tokenizers.
- q: Why must positional encoding be added to token embeddings before self-attention?
  options:
  - Because embeddings are too large to fit in memory otherwise
  - To convert the embeddings into integer token IDs
  - Because softmax requires positive inputs only
  - Because self-attention is permutation-invariant and has no inherent notion of token order
  answer: 3
  why: Self-attention treats its inputs as an unordered set, so without positional information the model
    could not tell 'dog bites man' from 'man bites dog'. Positional encoding injects order into the representations.
- q: In scaled dot-product attention, attention = softmax(Q Kᵀ / sqrt(d_k)) V, what is the role of dividing
    by sqrt(d_k)?
  options:
  - It converts the values matrix V into probabilities
  - It scales the dot products so the softmax gradients stay stable for large key dimensions
  - It replaces the need for the value matrix V
  - It guarantees the attention weights sum to the key dimension
  answer: 1
  why: For large d_k the dot products Q·K grow large in magnitude, pushing softmax into regions with tiny
    gradients. Dividing by sqrt(d_k) keeps the scores at a reasonable scale so learning remains stable.
- q: What does multi-head attention add compared to a single attention computation?
  options:
  - It removes the query and key projections entirely
  - It forces every head to learn identical weights
  - It runs several attention heads in parallel, each in its own subspace, then concatenates their outputs
  - It replaces attention with a recurrent loop
  answer: 2
  why: Multi-head attention projects Q, K, and V into several lower-dimensional subspaces and runs attention
    in each in parallel, letting different heads focus on different relationships, then concatenates and
    projects the results.
- q: In one or two sentences, explain how a base transformer gets scaled into a modern large language
    model (LLM).
  answer: By stacking many transformer (typically decoder) blocks with billions of parameters and pretraining
    on massive text corpora using a self-supervised objective such as next-token prediction.
  why: 'LLMs are transformers scaled up in depth, width, and data: many stacked blocks are pretrained
    with a self-supervised objective (e.g., next-token prediction or masked language modeling) over huge
    corpora, after which they can be fine-tuned or prompted for downstream tasks.'
resources:
- label: Attention Is All You Need (Vaswani et al., 2017)
  url: https://arxiv.org/abs/1706.03762
- label: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
- label: The Illustrated Transformer (Jay Alammar)
  url: https://jalammar.github.io/illustrated-transformer/
- label: 'Hugging Face: Summary of the Tokenizers'
  url: https://huggingface.co/docs/transformers/tokenizer_summary
---

## Overview

The transformer is the architecture behind every modern large language model, from BERT to GPT to the latest 2026 frontier systems. We follow a sentence from raw text into a transformer: it is **tokenized**, turned into **embeddings**, given **positional information**, then processed by **self-attention**. This path is the single most important step toward becoming an LLM engineer.

## 1. Why Transformers Replaced RNNs

Before 2017, sequence models were dominated by recurrent neural networks (RNNs, LSTMs, GRUs). They read text one token at a time, carrying a hidden state forward. This had two weaknesses:

- **No parallelism.** Each step depends on the previous one, so you cannot use a GPU's parallelism across the sequence during training.
- **Weak long-range memory.** Information from early tokens decays as it is passed through many steps, making it hard to connect words far apart.

The transformer, introduced in *Attention Is All You Need*, throws out recurrence entirely. Every token can attend to every other token **in a single parallel step**, so long-range dependencies are just one attention hop away and training scales beautifully on modern hardware.

## 2. Tokenization: Text to IDs

A model cannot consume raw characters; it needs integers. **Tokenization** splits text into tokens and maps each to an ID in a fixed vocabulary. Modern LLMs use **subword** tokenization (e.g., Byte-Pair Encoding), representing rare words as combinations of known pieces to avoid the out-of-vocabulary problem.

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("bert-base-uncased")
enc = tok("Hello world")
print(enc["input_ids"])      # e.g. [101, 7592, 2088, 102]
print(tok.tokenize("tokenization"))  # ['token', '##ization']
```

Notice that 'tokenization' splits into subword pieces. The special IDs 101 and 102 are the [CLS] and [SEP] markers BERT adds automatically.

## 3. Embeddings and Positional Encoding

Each token ID indexes into an **embedding table**, producing a dense vector (say 768 numbers) that the model can learn to shape into meaning. But self-attention treats its inputs as an unordered *set* — it is **permutation-invariant**. Without extra signal, the model could not distinguish 'dog bites man' from 'man bites dog'.

The fix is **positional encoding**: we add a position-dependent vector to each token embedding so order is baked in. The original paper uses fixed sinusoidal functions; modern models often learn positions or use rotary embeddings (RoPE). The key idea: **token embedding + positional encoding = the input to attention.**

## 4. Self-Attention: The Core Mechanism

Self-attention lets each token gather information from all others. From every token's embedding we derive three vectors via learned linear projections:

- **Query (Q)** — what this token is looking for.
- **Key (K)** — what each token offers.
- **Value (V)** — the actual content to be passed along.

We score how well each query matches each key with a dot product, scale by `sqrt(d_k)` to keep gradients stable, apply softmax to get weights that sum to 1, and use those weights to average the values:

```text
attention(Q, K, V) = softmax(Q K^T / sqrt(d_k)) V
```

Here is a faithful minimal NumPy implementation:

```python
import numpy as np

def attention(Q, K, V):
    scores = Q @ K.T / np.sqrt(K.shape[-1])
    weights = np.exp(scores) / np.exp(scores).sum(axis=-1, keepdims=True)  # softmax
    return weights @ V
```

The division by `sqrt(d_k)` matters: for large key dimensions the dot products grow large, pushing softmax into flat regions with vanishing gradients. Scaling keeps training healthy.

## 5. Multi-Head Attention and the Transformer Block

A single attention computation can only focus on one kind of relationship at a time. **Multi-head attention** runs several attention heads **in parallel**, each with its own Q/K/V projections into a smaller subspace. Their outputs are **concatenated** and linearly projected back. One head might track syntax, another coreference — the model learns a rich mix.

These heads sit inside a **transformer block**, which adds a position-wise feed-forward network plus **residual connections** and **layer normalization** to stabilize deep stacks. The original architecture pairs an **encoder** (bidirectional) with a **decoder** (masked, left-to-right). Encoder-only models like BERT excel at understanding; decoder-only models like GPT excel at generation.

## 6. From Transformers to LLMs

A large language model is, fundamentally, a transformer **scaled up**: stack dozens or hundreds of blocks, widen the layers to billions of parameters, and pretrain on enormous text corpora using a **self-supervised** objective — typically **next-token prediction** for decoder-only models or **masked language modeling** for encoder-only ones. No human labels are required; the text supervises itself.

This scaling, combined with vast data, produces the emergent capabilities we associate with modern LLMs. Once pretrained, the same model can be **fine-tuned** or **prompted** for countless downstream tasks — the foundation for the rest of this module.

## Key Takeaways

Transformers replaced RNNs by enabling parallelism and direct long-range attention. Text becomes subword tokens, then embeddings plus positional encoding, then flows through self-attention — `softmax(Q K^T / sqrt(d_k)) V` — generalized into multi-head attention inside stacked blocks. Scale that with self-supervised pretraining and you get a large language model.
