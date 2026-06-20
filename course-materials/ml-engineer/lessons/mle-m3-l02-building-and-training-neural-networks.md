---
course: ml-engineer
title: Building and Training Neural Networks
month: 3
monthTitle: Deep Learning with PyTorch
lesson: 2
summary: Learn to build, train, and tune a feedforward neural network in PyTorch using nn.Module, Dataset/DataLoader,
  an optimizer, and a loss function, then evaluate it on a real dataset with proper train/validation splits.
objectives:
- Define a feedforward neural network by subclassing torch.nn.Module
- Load and batch real data efficiently with Dataset and DataLoader
- Implement a complete training loop with forward pass, loss, backprop, and optimizer step
- Evaluate models correctly using eval mode and torch.no_grad
- Apply tuning techniques (learning rate, batch size, regularization) to improve generalization
- Save and reload trained model weights for reuse
video: mle-m3-l02-building-and-training-neural-networks.mp4
quiz:
- q: Why do we typically output raw logits from the model instead of applying softmax?
  options:
  - Softmax is too slow to compute
  - nn.CrossEntropyLoss applies log-softmax internally
  - Logits are required by DataLoader
  - Softmax cannot be backpropagated
  answer: 1
  why: nn.CrossEntropyLoss combines log-softmax and negative log-likelihood, so applying softmax yourself
    would double-apply the transformation and hurt training.
- q: What is the purpose of calling optimizer.zero_grad() in the training loop?
  options:
  - It resets the model weights
  - It clears accumulated gradients from the previous step
  - It shuffles the data
  - It switches the model to eval mode
  answer: 1
  why: PyTorch accumulates gradients by default, so you must zero them each iteration or gradients from
    prior batches will contaminate the current update.
- q: Which mode and context should wrap your evaluation loop?
  options:
  - model.train() and torch.enable_grad()
  - model.eval() and torch.no_grad()
  - model.eval() and torch.enable_grad()
  - model.train() and torch.no_grad()
  answer: 1
  why: model.eval() disables dropout and uses running batchnorm stats, while torch.no_grad() avoids tracking
    gradients for faster, memory-efficient inference.
- q: Why should feature standardization statistics be computed only on the training set?
  options:
  - To make training faster
  - To prevent data leakage from validation/test into the model
  - Because validation data has no features
  - To increase the batch size
  answer: 1
  why: Using validation or test statistics leaks information about unseen data into preprocessing, producing
    overly optimistic and invalid performance estimates.
- q: In one short phrase, which hyperparameter generally has the largest effect on training and should
    be tuned first?
  answer: learning rate
  why: The learning rate controls step size during optimization; too high diverges and too low stalls,
    making it the most impactful hyperparameter to tune first.
- q: What object should you save for a portable model checkpoint in PyTorch?
  answer: the state_dict
  why: Saving model.state_dict() stores just the learned parameters, which is more portable and robust
    across code changes than pickling the entire model object.
resources:
- label: 'PyTorch Official Tutorials: Learn the Basics'
  url: https://pytorch.org/tutorials/beginner/basics/intro.html
- label: torch.nn Module Documentation
  url: https://pytorch.org/docs/stable/nn.html
- label: 'PyTorch Data Loading: Dataset and DataLoader'
  url: https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
- label: Deep Learning with PyTorch (Free Book PDF)
  url: https://pytorch.org/assets/deep-learning/Deep-Learning-with-PyTorch.pdf
---

## Overview

In this lesson you will build a feedforward (fully connected) neural network in PyTorch and train it end-to-end on a real tabular dataset. We cover the four pillars of any PyTorch training pipeline: **the model**, **the data**, **the loss function**, and **the optimizer**.

## 1. The Model: subclassing nn.Module

Every network in PyTorch is a subclass of `nn.Module`. You define layers in `__init__` and the data flow in `forward`.

```python
import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, in_features, hidden, n_classes):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_features, hidden),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden, n_classes),
        )
    def forward(self, x):
        return self.net(x)  # raw logits
```

Note we output **raw logits** (no softmax) because `nn.CrossEntropyLoss` applies log-softmax internally.

## 2. The Data: Dataset and DataLoader

A `Dataset` knows how to return a single `(features, label)` pair. A `DataLoader` wraps it to provide batching, shuffling, and parallel loading.

```python
from torch.utils.data import TensorDataset, DataLoader

train_ds = TensorDataset(X_train, y_train)
train_dl = DataLoader(train_ds, batch_size=64, shuffle=True)
val_dl   = DataLoader(val_ds, batch_size=256, shuffle=False)
```

Always **shuffle the training set** and never shuffle validation/test. Standardize numeric features (zero mean, unit variance) using statistics computed only on the training split to avoid data leakage.

## 3. Loss and Optimizer

```python
model = MLP(in_features=20, hidden=64, n_classes=2)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
```

`weight_decay` adds L2 regularization. Adam is a solid default optimizer; SGD with momentum can generalize better but needs more tuning.

## 4. The Training Loop

The core cycle for every batch: zero gradients → forward → compute loss → backward → step.

```python
for epoch in range(epochs):
    model.train()
    for xb, yb in train_dl:
        optimizer.zero_grad()
        logits = model(xb)
        loss = criterion(logits, yb)
        loss.backward()
        optimizer.step()
```

`optimizer.zero_grad()` is essential because PyTorch **accumulates** gradients by default; forgetting it is a classic bug.

## 5. Evaluation

Use `model.eval()` to disable dropout/batchnorm updates, and `torch.no_grad()` to skip gradient tracking for speed and memory.

```python
model.eval()
correct = 0
with torch.no_grad():
    for xb, yb in val_dl:
        preds = model(xb).argmax(dim=1)
        correct += (preds == yb).sum().item()
acc = correct / len(val_ds)
```

## 6. Tuning for Better Generalization

- **Learning rate** is the most important hyperparameter. Try a sweep (1e-2, 1e-3, 1e-4).
- **Batch size** trades stability vs. speed; larger batches may need a larger LR.
- **Regularization**: dropout, weight decay, and early stopping fight overfitting.
- **Monitor the gap** between training and validation loss; a widening gap signals overfitting.

## 7. Saving and Loading

```python
torch.save(model.state_dict(), 'model.pt')
model.load_state_dict(torch.load('model.pt'))
model.eval()
```

Save the `state_dict` (the learned parameters), not the whole object, for portability.

## Key Takeaways

A PyTorch pipeline always combines model, data, loss, and optimizer. Master the zero_grad → forward → loss → backward → step rhythm, separate train/eval modes properly, and tune the learning rate first.
