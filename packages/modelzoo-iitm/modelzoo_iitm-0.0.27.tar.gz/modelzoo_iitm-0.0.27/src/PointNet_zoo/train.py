import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import os
import json
import glob 
import gc
import time
import torch.optim as optim
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import numpy as np
import matplotlib.pyplot as plt
from torch.autograd import Variable
from PointNet_zoo.model import *

epoch_train_losses = []  
epoch_test_losses = []
epoch_val_losses = []              
accu_train_epoch = []
accu_test_epoch = []
accu_val_epoch = []

batch_size = 32
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = Point_Net(T_Net).to(device)
model = model.apply(weights_init)

epochs = 20
lr = 0.001
model = model.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr, eps=1e-08, weight_decay= 1e-4)

def feature_transform_regularizer(trans):
    d = trans.size()[1]
    batchsize = trans.size()[0]
    I = torch.eye(d)[None, :, :]
    if trans.is_cuda:
        I = I.cuda()
    loss = torch.mean(torch.norm(torch.bmm(trans, trans.transpose(2,1)) - I, dim=(1,2)))
    return loss

def criterion(pred, target, trans_feat):
        loss = F.nll_loss(pred, target)
        mat_diff_loss = feature_transform_regularizer(trans_feat)
        total_loss = loss + mat_diff_loss * 0.001
        return total_loss

def accuracy(y_pred, y):
    _, predicted = torch.max(y_pred, 1)
    correct = (predicted == y).sum().item()
    return correct/(batch_size*2048)

def make_tensor(tensor):
  if torch.cuda.is_available():
    return torch.cuda.FloatTensor(tensor)
  else:
    return torch.FloatTensor(tensor)

def train_PointNet(model, dataset, optimizer, device):

    train_loss_batch = []
    accu_train_batch = []
    model.train()
    for idx,(data, labels, seg) in enumerate(dataset):
        optimizer.zero_grad()
        data = data.to(device)
        labels = labels.to(device)
        seg = seg.to(device)
        #Forward Pass
        data = data.float()
        labels = labels.long()
        seg = seg.long()
        data = data.transpose(2, 1)

        output, A = model(data, to_categorical(labels, 16))
        A = A.to(device)
        output = output.contiguous().view(-1, 50)
        seg = seg.view(-1, 1)[:, 0]
        pred_choice = output.data.max(1)[1]
        correct = pred_choice.eq(seg.data).cpu().sum()
        accu_train_batch.append(correct.item() / (batch_size * 2048))
        train_loss = criterion(output, seg, A)
        train_loss_batch.append(train_loss.item())
        # Backward
        train_loss.backward()
        optimizer.step()
    epoch_train_losses.append(sum(train_loss_batch)/len(dataset))
    accu_train_epoch.append(sum(accu_train_batch)/len(dataset))
    print(f"Train Epoch Loss: {sum(train_loss_batch)/len(dataset):.5f}   Train Epoch Accuracy: {sum(accu_train_batch)/len(dataset)*100:.5f}")

def val_PointNet(model, dataset, device):
    
    val_loss_batch = []
    accu_val_batch = []
    model.eval()
    for idx,(data, labels, seg) in enumerate(dataset):
      with torch.no_grad():
        data = data.to(device)
        labels = labels.to(device)
        seg = seg.to(device)
        #Forward Pass
        data = data.float()
        labels = labels.long()
        seg = seg.long()
        data = data.transpose(2, 1)

        output, A = model(data, to_categorical(labels, 16))
        A = A.to(device)
        output = output.contiguous().view(-1, 50)
        seg = seg.view(-1, 1)[:, 0]
        pred_choice = output.data.max(1)[1]
        correct = pred_choice.eq(seg.data).cpu().sum()
        accu_val_batch.append(correct.item() / (batch_size * 2048))
        val_loss = criterion(output, seg, A)
        val_loss_batch.append(val_loss.item())
    epoch_val_losses.append((sum(val_loss_batch))/len(dataset))
    accu_val_epoch.append((sum(accu_val_batch))/len(dataset))
    print(f"Val Epoch Loss: {(sum(val_loss_batch))/len(dataset):.5f} Val Epoch Accuracy: {(sum(accu_val_batch))/len(dataset)*100:.5f}")