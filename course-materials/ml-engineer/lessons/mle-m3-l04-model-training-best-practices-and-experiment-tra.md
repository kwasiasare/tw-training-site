---
course: ml-engineer
title: Model Training Best Practices and Experiment Tracking
month: 3
monthTitle: Deep Learning with PyTorch
lesson: 4
summary: A practical guide to training robust PyTorch models efficiently using learning rate schedules,
  early stopping, regularization techniques, and systematic experiment tracking.
objectives:
- Apply learning rate schedules (step, cosine, ReduceLROnPlateau, warmup) to improve convergence
- Implement early stopping to prevent overfitting and save compute
- Use regularization techniques including weight decay, dropout, and data augmentation
- Set up experiment tracking with tools like Weights & Biases or TensorBoard
- Organize training runs reproducibly with config management and seeding
- Diagnose training problems by reading loss/metric curves
video: mle-m3-l04-model-training-best-practices-and-experiment-tra.mp4
quiz:
- q: Which scheduler adapts the learning rate based on a monitored metric rather than a fixed schedule?
  options:
  - StepLR
  - CosineAnnealingLR
  - ReduceLROnPlateau
  - LinearLR
  answer: 2
  why: ReduceLROnPlateau lowers the LR only when a monitored metric (e.g., validation loss) stops improving,
    making it adaptive rather than schedule-based.
- q: In an early stopping setup, which checkpoint should you ultimately use?
  options:
  - The last epoch's weights
  - The best validation-metric weights saved during training
  - The first epoch's weights
  - A random epoch
  answer: 1
  why: Validation performance often peaks before the final epoch, so you save and use the best checkpoint,
    not the last.
- q: Why is AdamW preferred over Adam when applying weight decay?
  options:
  - It trains faster on GPUs
  - It decouples weight decay from the gradient update
  - It removes the need for a learning rate
  - It disables dropout automatically
  answer: 1
  why: AdamW decouples weight decay from the adaptive gradient update, applying true L2 regularization
    correctly, unlike standard Adam.
- q: What is the main purpose of learning rate warmup?
  options:
  - To overfit faster
  - To stabilize early training, especially for transformers and large batches
  - To replace data augmentation
  - To stop training early
  answer: 1
  why: Warmup starts with a small LR and ramps it up, preventing instability in the early, sensitive steps
    of training.
- q: Name one thing you should seed to make a PyTorch training run reproducible.
  answer: torch.manual_seed (also numpy and random)
  why: Seeding torch, numpy, and Python's random module controls stochastic operations so runs can be
    reproduced.
- q: What does torch.nn.utils.clip_grad_norm_ help prevent?
  answer: Exploding gradients
  why: Gradient clipping caps the gradient norm, preventing unstable, exploding gradient updates.
resources:
- label: PyTorch LR Scheduler Documentation
  url: https://pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate
- label: Weights & Biases PyTorch Integration Guide
  url: https://docs.wandb.ai/guides/integrations/pytorch
- label: PyTorch Reproducibility Notes
  url: https://pytorch.org/docs/stable/notes/randomness.html
- label: Decoupled Weight Decay Regularization (AdamW paper)
  url: https://arxiv.org/abs/1711.05101
---

## Why Training Best Practices Matter

Getting a model to *learn* is easy; getting it to learn **robustly and efficiently** is the engineering challenge. This lesson covers the practical levers a Machine Learning Engineer pulls during training: schedules, stopping criteria, regularization, and the tracking discipline that makes results reproducible and comparable.

## Learning Rate Schedules

The learning rate (LR) is the single most important hyperparameter. A fixed LR is rarely optimal: too high and training diverges, too low and it crawls. Schedules adjust LR over time.

- **Step decay**: drop LR by a factor every N epochs (`StepLR`, `MultiStepLR`).
- **Cosine annealing**: smoothly decay following a cosine curve (`CosineAnnealingLR`). Popular and strong default.
- **ReduceLROnPlateau**: drop LR when a monitored metric stops improving — adaptive, no schedule guessing.
- **Warmup**: start LR small and ramp up over the first few hundred steps to stabilize early training (essential for transformers and large batches).

```python
import torch
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-2)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=num_epochs)
for epoch in range(num_epochs):
    train_one_epoch(...)
    scheduler.step()   # step per epoch for CosineAnnealingLR
```

For `ReduceLROnPlateau` you call `scheduler.step(val_loss)` after validation. Always confirm whether a scheduler steps per-batch or per-epoch.

## Early Stopping

Early stopping halts training when validation performance stops improving, preventing overfitting and saving compute. The pattern: track the best validation metric, count epochs without improvement (`patience`), and stop when patience is exceeded. Always save the **best** checkpoint, not just the last.

```python
best_loss, patience, wait = float('inf'), 5, 0
for epoch in range(max_epochs):
    val_loss = validate(...)
    if val_loss < best_loss - 1e-4:
        best_loss, wait = val_loss, 0
        torch.save(model.state_dict(), 'best.pt')
    else:
        wait += 1
        if wait >= patience:
            print('Early stopping'); break
```

## Regularization

Regularization fights overfitting by constraining model complexity:

- **Weight decay (L2)**: penalizes large weights. Use `AdamW` so decay is decoupled from the gradient update.
- **Dropout**: randomly zeroes activations during training. Remember `model.train()` vs `model.eval()` toggles it.
- **Data augmentation**: expands effective dataset size (flips, crops, noise) — often the highest-impact regularizer.
- **Batch/Layer normalization**: stabilizes and regularizes indirectly.
- **Gradient clipping**: `torch.nn.utils.clip_grad_norm_` prevents exploding gradients.

## Experiment Tracking

When you run dozens of experiments, memory and spreadsheets fail. Use a tracking tool (Weights & Biases, MLflow, or TensorBoard) to log hyperparameters, metrics, and artifacts automatically.

```python
import wandb
wandb.init(project='img-classifier', config={'lr':1e-3,'bs':64})
for epoch in range(num_epochs):
    train_loss = train_one_epoch(...)
    val_loss = validate(...)
    wandb.log({'train_loss':train_loss,'val_loss':val_loss,
               'lr':optimizer.param_groups[0]['lr']})
```

**Reproducibility checklist**: seed everything (`torch.manual_seed`, `numpy`, `random`), log the exact config, pin dependency versions, and version your data. A run you can't reproduce is a run you can't trust.

## Putting It Together

A solid training loop combines all four: an AdamW optimizer with weight decay, a cosine or plateau scheduler, early stopping on validation loss, augmentation in the data pipeline, and every metric streamed to your tracker. This is the baseline professional MLEs ship.
