# -*- coding: utf-8 -*-
"""slp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1k4isdOw0HIVyEUPv3IAZhZEI0jjc2gjl
"""

import torch
import torch.nn as nn
import torch.optim as optim

torch.manual_seed(42)

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc = nn.Linear(1, 1)  # Single layer perceptron with 1D input and 1D output

    def forward(self, x):
        out = self.fc(x)  # Pass input through the fully connected layer
        return out

net = Net()
optimizer = optim.SGD(net.parameters(), lr=0.01)  # Learning rate of 0.01 for SGD

X = 2 * torch.rand(100) - 1  # X within range of [-1, 1]
Y = X * 3.0 + 1

for epoch in range(10):  # Iterating through 10 epochs
    epoch_loss = 0
    for i, (x, y) in enumerate(zip(X, Y)):
        x = torch.unsqueeze(x, 0)  # Changing tensor(1.) to tensor([1.])
        y = torch.unsqueeze(y, 0)  # Changing tensor(4.) to tensor([4.])

        optimizer.zero_grad()  # Zero the gradients

        output = net(x)  # Forward pass

        loss = nn.MSELoss()(output, y)  # Calculate MSE loss between output and target
        loss.backward()  # Backpropagation
        optimizer.step()  # Update the weights

        epoch_loss += loss.item()

    print("Epoch {} - loss: {}".format(epoch + 1, epoch_loss))

# Check the learned parameters
for name, param in net.named_parameters():
    if "weight" in name:
        w = round(param.item(), 1)
    if "bias" in name:
        b = round(param.item(), 1)

print("Learned Weight:", w)
print("Learned Bias:", b)