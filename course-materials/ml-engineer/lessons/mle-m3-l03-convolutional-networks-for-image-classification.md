---
course: ml-engineer
title: Convolutional Networks for Image Classification
month: 3
monthTitle: Deep Learning with PyTorch
lesson: 3
summary: Learn to design, train, and improve convolutional neural networks (CNNs) for image classification
  in PyTorch. This lesson covers the core building blocks of CNNs, a practical training loop, data augmentation,
  and transfer learning to boost accuracy with limited data.
objectives:
- Explain the role of convolution, pooling, and fully connected layers in a CNN
- Build and train a CNN image classifier in PyTorch using a standard training loop
- Apply data augmentation with torchvision transforms to reduce overfitting
- Use transfer learning by fine-tuning a pretrained model (e.g., ResNet) on a new dataset
- Evaluate model performance and diagnose overfitting vs. underfitting
video: mle-m3-l03-convolutional-networks-for-image-classification.mp4
quiz:
- q: What two key ideas allow CNNs to use far fewer parameters than fully connected networks on images?
  options:
  - Dropout and batch normalization
  - Local connectivity and weight sharing
  - Softmax and cross-entropy
  - Pooling and padding
  answer: 1
  why: Local connectivity means each neuron only sees a small region, and weight sharing reuses the same
    filter across the image, drastically reducing parameters while giving translation invariance.
- q: In PyTorch, what input does nn.CrossEntropyLoss expect from the model?
  options:
  - Softmax probabilities
  - Raw logits (no softmax applied)
  - One-hot encoded predictions
  - Log-probabilities only
  answer: 1
  why: CrossEntropyLoss applies log-softmax internally, so you pass raw logits and integer class labels;
    applying softmax yourself would be incorrect.
- q: Why should data augmentation be applied only to the training set?
  options:
  - It is too slow for validation
  - Validation/test should measure performance on unaltered, representative data
  - Augmentation requires gradients
  - It changes the number of classes
  answer: 1
  why: Augmentation adds randomness to expand training variety, but validation and test sets must be deterministic
    to give a fair, reproducible measure of real-world performance.
- q: When doing transfer learning as pure feature extraction, what do you do with the pretrained backbone?
  options:
  - Reinitialize it randomly
  - Freeze it (requires_grad=False) and train only the new head
  - Train it with a large learning rate
  - Delete all but the first layer
  answer: 1
  why: In feature extraction you freeze the backbone so its learned features stay fixed, and only the
    newly added classification head is trained.
- q: Your model shows 98% training accuracy but only 70% validation accuracy. Name the problem and one
    fix.
  answer: Overfitting; fix with more data augmentation, dropout, weight decay, or early stopping.
  why: A large gap between high train accuracy and lower validation accuracy indicates overfitting, addressed
    by stronger regularization or more/augmented data.
- q: What does a MaxPool2d(2) layer do to a feature map?
  answer: It downsamples the spatial dimensions by a factor of 2, keeping the maximum value in each 2x2
    region.
  why: Max pooling reduces spatial resolution and computation while retaining the strongest activations,
    adding robustness to small translations.
resources:
- label: PyTorch Transfer Learning Tutorial
  url: https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html
- label: torchvision.transforms documentation
  url: https://pytorch.org/vision/stable/transforms.html
- label: 'CS231n: Convolutional Neural Networks'
  url: https://cs231n.github.io/convolutional-networks/
- label: torchvision.models (pretrained models)
  url: https://pytorch.org/vision/stable/models.html
---

## Why Convolutional Networks?

Fully connected networks treat each pixel independently and ignore spatial structure. Images have local patterns (edges, textures) that repeat across the image. **Convolutional Neural Networks (CNNs)** exploit this with two key ideas:

- **Local connectivity**: each neuron looks at a small region (the receptive field).
- **Weight sharing**: the same filter slides across the whole image, drastically reducing parameters and giving translation invariance.

## Core Building Blocks

- **Convolution layer (`nn.Conv2d`)**: learns a set of filters (kernels). Key args: `in_channels`, `out_channels`, `kernel_size`, `stride`, `padding`.
- **Activation (`ReLU`)**: introduces non-linearity.
- **Pooling (`nn.MaxPool2d`)**: downsamples spatially, reducing resolution and computation while adding robustness.
- **Batch Normalization (`nn.BatchNorm2d`)**: stabilizes and speeds up training.
- **Fully connected head (`nn.Linear`)**: maps extracted features to class scores.

A typical block is: `Conv -> BatchNorm -> ReLU -> Pool`, stacked several times, then flattened into a classifier head.

## A Simple CNN in PyTorch

```python
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(),
            nn.MaxPool2d(2),
        )
        # AdaptiveAvgPool2d collapses each channel to 1x1 for ANY input size,
        # so the flatten dim is always 64 (the channel count) — no shape errors.
        # Without it, flatten dim = channels * H * W after the convs, e.g. a
        # 32x32 input -> two /2 pools -> 64*8*8 = 4096; a 224x224 input -> 64*56*56.
        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64, 128), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )
    def forward(self, x):
        return self.classifier(self.pool(self.features(x)))
```

## The Training Loop

```python
import torch
model = SimpleCNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

for epoch in range(epochs):
    model.train()
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    # validation pass with model.eval() and torch.no_grad()
```

Note: `CrossEntropyLoss` expects raw logits (no softmax) and integer class labels.

## Data Augmentation

Augmentation creates new training examples by transforming images, which reduces overfitting and improves generalization. Apply augmentation **only to the training set**; keep validation/test deterministic.

```python
from torchvision import transforms

train_tf = transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.2, 0.2, 0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
val_tf = transforms.Compose([
    transforms.Resize(256), transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
```

## Transfer Learning

Training from scratch needs lots of data and compute. **Transfer learning** reuses a model pretrained on ImageNet and adapts it to your task.

```python
from torchvision import models

model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in model.parameters():
    p.requires_grad = False          # freeze backbone (feature extraction)
model.fc = nn.Linear(model.fc.in_features, num_classes)  # new head trains
```

Two common strategies:

- **Feature extraction**: freeze the backbone, train only the new head. Fast, great for small datasets.
- **Fine-tuning**: unfreeze some or all layers and train with a small learning rate (e.g., `1e-4`) so pretrained weights aren't destroyed.

## Evaluating and Diagnosing

- Track **training vs. validation accuracy/loss** each epoch.
- **Overfitting**: train accuracy high, val accuracy low — add augmentation, dropout, or weight decay.
- **Underfitting**: both low — train longer, increase capacity, or reduce regularization.
- Inspect a **confusion matrix** to find which classes are confused.

## Practical Tips

- Always normalize inputs with the same statistics the pretrained model used.
- Use a GPU; move both model and tensors to `device`.
- Save checkpoints with `torch.save(model.state_dict())`.
- Use a learning rate scheduler (e.g., `StepLR`, `CosineAnnealingLR`) for better convergence.
