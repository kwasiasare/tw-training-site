---
course: ml-engineer
title: 'PyTorch Fundamentals: Tensors and Autograd'
month: 3
monthTitle: Deep Learning with PyTorch
lesson: 1
summary: 'Learn PyTorch''s core building blocks: tensors and automatic differentiation. You''ll create
  and manipulate tensors, understand the autograd engine, and implement gradient descent from scratch
  to fit a simple model.'
objectives:
- Create, reshape, and perform operations on PyTorch tensors
- Move tensors between CPU and GPU and convert to/from NumPy
- Explain how autograd builds a computation graph and computes gradients
- Use requires_grad, .backward(), and .grad to obtain gradients
- Implement gradient descent manually to fit a linear model
- Apply torch.no_grad() and zero_grad practices to write correct training loops
video: mle-m3-l01-pytorch-fundamentals-tensors-and-autograd.mp4
quiz:
- q: What does setting requires_grad=True on a tensor do?
  options:
  - Moves the tensor to the GPU
  - Tells PyTorch to track operations so gradients can be computed
  - Converts the tensor to a NumPy array
  - Makes the tensor immutable
  answer: 1
  why: requires_grad=True signals autograd to record operations on the tensor into the computation graph
    so .backward() can compute gradients.
- q: Why must you call zero_grad (or .grad.zero_()) each training iteration?
  options:
  - To reset the model weights
  - Because gradients accumulate across backward calls
  - To move data to the GPU
  - To convert gradients to floats
  answer: 1
  why: PyTorch accumulates gradients into .grad on each backward call, so they must be cleared between
    steps or they pile up and corrupt updates.
- q: Why are parameter updates wrapped in torch.no_grad()?
  options:
  - To speed up the forward pass
  - To prevent the update operations from being tracked in the computation graph
  - To enable GPU acceleration
  - To compute second derivatives
  answer: 1
  why: Updates change parameter values; without no_grad these in-place operations would be recorded by
    autograd, corrupting the graph.
- q: What is required for .backward() to work without extra arguments?
  options:
  - The tensor must be on the GPU
  - The output must be a scalar
  - The tensor must be an integer type
  - requires_grad must be False
  answer: 1
  why: backward() computes gradients of a scalar with respect to inputs; for non-scalar outputs you must
    pass a gradient tensor.
- q: In one sentence, what does loss.backward() do in a training loop?
  answer: It computes the gradients of the loss with respect to all tensors with requires_grad=True and
    stores them in their .grad attributes.
  why: backward() traverses the computation graph in reverse applying the chain rule, populating each
    parameter's .grad.
- q: What attribute tells you which device (CPU or GPU) a tensor lives on?
  answer: .device
  why: Every tensor exposes a .device attribute; operations require tensors on the same device.
resources:
- label: 'PyTorch Official Tutorial: Tensors'
  url: https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html
- label: PyTorch Autograd Mechanics
  url: https://pytorch.org/docs/stable/notes/autograd.html
- label: 'Deep Learning with PyTorch: A 60 Minute Blitz'
  url: https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html
---

## Why Tensors and Autograd Matter

Every deep learning model in PyTorch is built on two foundations: **tensors** (the data structure that holds numbers) and **autograd** (the engine that computes gradients automatically). Master these and the rest of PyTorch becomes far easier.

## Tensors: The Core Data Structure

A tensor is an n-dimensional array, similar to a NumPy array but with two superpowers: it can live on a GPU and it can track gradients.

```python
import torch

# Creating tensors
a = torch.tensor([1.0, 2.0, 3.0])      # from data
z = torch.zeros(2, 3)                   # 2x3 of zeros
r = torch.randn(2, 3)                   # random normal

print(a.shape, a.dtype, a.device)
```

### Common Operations

```python
x = torch.randn(2, 3)
x.sum(), x.mean()            # reductions
x.reshape(3, 2)              # change shape
x.T                          # transpose
x @ x.T                      # matrix multiply
x + 1                        # broadcasting
```

Broadcasting lets tensors of different shapes combine by automatically expanding dimensions, just like NumPy.

### GPU and NumPy Interop

```python
if torch.cuda.is_available():
    x = x.to('cuda')         # move to GPU

import numpy as np
n = x.cpu().numpy()          # tensor -> numpy
t = torch.from_numpy(n)      # numpy -> tensor (shares memory)
```

## Autograd: Automatic Differentiation

When you set `requires_grad=True`, PyTorch records every operation into a **dynamic computation graph**. Calling `.backward()` on a scalar walks this graph backward applying the chain rule, storing gradients in each tensor's `.grad` attribute.

```python
x = torch.tensor(2.0, requires_grad=True)
y = x ** 2 + 3 * x          # y = x^2 + 3x
y.backward()                # compute dy/dx
print(x.grad)               # 2x + 3 = 7.0
```

Key points:
- `.backward()` requires a scalar output (or you must pass a gradient argument).
- Gradients **accumulate** in `.grad`, so you must zero them between steps.
- Wrap inference or parameter updates in `torch.no_grad()` to avoid tracking.

## Implementing Gradient Descent from Scratch

Let's fit `y = w*x + b` to data using nothing but tensors and autograd.

```python
import torch

# Synthetic data: true relationship y = 2x + 1
X = torch.linspace(0, 1, 100).reshape(-1, 1)
y = 2 * X + 1 + 0.1 * torch.randn_like(X)

# Parameters to learn
w = torch.randn(1, requires_grad=True)
b = torch.randn(1, requires_grad=True)
lr = 0.1

for epoch in range(200):
    y_pred = X * w + b                  # forward pass
    loss = ((y_pred - y) ** 2).mean()   # MSE loss

    loss.backward()                     # compute gradients

    with torch.no_grad():               # update without tracking
        w -= lr * w.grad
        b -= lr * b.grad
        w.grad.zero_()                  # reset gradients
        b.grad.zero_()

print(w.item(), b.item())               # ~2.0 and ~1.0
```

### The Anatomy of a Training Loop
1. **Forward pass** — compute predictions.
2. **Loss** — measure error with a scalar.
3. **Backward pass** — `loss.backward()` fills `.grad`.
4. **Update** — adjust parameters in the negative gradient direction.
5. **Zero gradients** — clear `.grad` for the next iteration.

This exact pattern, with `torch.optim` and `nn.Module` layered on top, powers every PyTorch model you'll build later.

## Common Pitfalls
- Forgetting `zero_grad()` causes gradients to pile up and training to diverge.
- Updating parameters outside `torch.no_grad()` adds the update to the graph.
- Calling `.backward()` on a non-scalar without a gradient argument raises an error.
- Mixing tensors on different devices (CPU vs GPU) throws errors.
