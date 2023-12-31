# -*- coding: utf-8 -*-
"""cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NE_ZO9rhWO9wE2IfNjEBXgi_wT39d9f_
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, recall_score, precision_score
import torch.nn.functional as F


# Data Preprocessing
transform = transforms.Compose([
    transforms.Resize((100, 100)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

dataset_path = './petimages'
dataset = datasets.ImageFolder(root=dataset_path, transform=transform)

n_test = int(len(dataset) * 0.2)  # 20% for testing
test_set, train_set = torch.utils.data.random_split(dataset, [n_test, len(dataset) - n_test])

batch_size = 32
trainloader = torch.utils.data.DataLoader(train_set, batch_size=batch_size, shuffle=True)
testloader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False)

# Define CNN model
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3)
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3)
        self.fc1 = nn.Linear(128 * 10 * 10, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = x.view(-1, 128 * 10 * 10)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

device = 'cuda' if torch.cuda.is_available() else 'cpu'
cnn = CNN().to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(cnn.parameters(), lr=0.0001)

# Training
epoch_size = 5
cnn.train()
for epoch in range(epoch_size):
    loss_val = 0.0
    for i, (inputs, labels) in enumerate(trainloader):
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = cnn(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        loss_val += loss.item()
        if i % 100 == 99:
            print(f'[{epoch + 1}, {i + 1:5d}] loss: {loss_val / 100:.3f}')
            loss_val = 0.0

print('Finished Training')

# Evaluation
ground_truth = []
predictions = []
cnn.eval()
with torch.no_grad():
    for data in testloader:
        inputs, labels = data
        inputs = inputs.to(device)
        outputs = cnn(inputs)
        _, predicted = torch.max(outputs.data, 1)
        ground_truth.extend(labels.tolist())
        predictions.extend(predicted.tolist())

accuracy = accuracy_score(ground_truth, predictions)
recall = recall_score(ground_truth, predictions, average='weighted')
precision = precision_score(ground_truth, predictions, average='weighted')

print('Accuracy:', accuracy)
print('Recall:', recall)
print('Precision:', precision)









