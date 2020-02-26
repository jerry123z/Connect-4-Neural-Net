import torch
import torch.nn as nn
import torch.nn.functional as f
from torch.utils.data import Dataset
import numpy as np


class ConvBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.action_size = 7
        self.conv1 = nn.Conv2d(1, 128, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(128)

    def forward(self, x):
        x = x.view(-1, 3, 6, 7)  # batch_size x channels x board_x x board_y
        x = f.relu(self.bn1(self.conv1(x)))
        return x


class ResBlock(nn.Module):
    def __init__(self, inplanes=128, planes=128, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride,
                               padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = f.relu(self.bn1(out))
        out = self.conv2(out)
        out = self.bn2(out)
        out += residual
        out = f.relu(out)
        return out


class OutBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(128, 3, kernel_size=1)  # value
        self.bn1 = nn.BatchNorm2d(3)
        self.fc1 = nn.Linear(3 * 6 * 7, 32)
        self.fc2 = nn.Linear(32, 1)

        self.conv2 = nn.Conv2d(128, 32, kernel_size=1)  # policy
        self.bn2 = nn.BatchNorm2d(32)
        self.logsoftmax = nn.LogSoftmax(dim=1)
        self.fc3 = nn.Linear(6 * 7 * 32, 7)  # mapping ( channels * height * width ) => width

    def forward(self, x):
        v = f.relu(self.bn1(self.conv1(x)))  # value
        v = v.view(-1, 3 * 6 * 7)  # batch_size, (channels * height * width) 2d array
        v = f.relu(self.fc1(v))
        v = torch.tanh(self.fc2(v))

        p = f.relu(self.bn2(self.conv2(x)))  # policy
        p = p.view(-1, 6 * 7 * 32)  # batch_size, (height * width * 32 filters) 2d array
        p = self.fc3(p)
        p = self.logsoftmax(p).exp()
        return p, v


class AlphaZero(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = ConvBlock()
        for block in range(7):
            setattr(self, "res_%i" % block, ResBlock())
        self.out = OutBlock()

    def forward(self, x):
        x = self.conv(x)
        for block in range(7):
            x = getattr(self, "res_%i" % block)(x)
        x = self.out(x)
        return x


class AlphaLoss(torch.nn.Module):
    def __init__(self):
        super(AlphaLoss, self).__init__()

    def forward(self, t_value, value, t_policy, policy):
        value_error = (value - t_value) ** 2
        policy_error = torch.sum((-policy * (1e-8 + t_policy.float()).float().log()), 1)
        total_error = (value_error.view(-1).float() + policy_error).mean()
        return total_error
