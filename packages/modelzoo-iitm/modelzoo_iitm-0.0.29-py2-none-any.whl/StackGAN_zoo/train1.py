import pandas as pd
import numpy as np
import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
from torchvision.utils import save_image
from PIL import Image
import PIL
import pickle
from torch.utils.data import Dataset
from glob import glob
import time
import gc
from torch.utils.data import DataLoader
from torch.utils.data import random_split
from torchvision.utils import make_grid
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer, util
from StackGAN_zoo.model import *


batch_size = 64
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

StageI_Gen = StageI_GAN_Gen(Conditioning_Augmentation_StageI).to(device)
StageI_Gen = StageI_Gen.apply(weights_init)
StageI_Dis = StageI_GAN_Dis(DownSample1).to(device)
StageI_Dis = StageI_Dis.apply(weights_init)
sbert_model = SentenceTransformer('paraphrase-mpnet-base-v2')

epoch_D1losses = []             
epoch_G1losses = []
epoch_D2losses = []             
epoch_G2losses = []
epoch_Real_Score = []
epoch_Fake_Score = []
epoch_Generator_Score = []


epochs = 600
lrG = 0.00002
lrD = 0.0002

optimizerD1 = torch.optim.Adam(StageI_Dis.parameters(), lr=lrD, betas=(0.5,0.999))
optimizerG1 = torch.optim.Adam(StageI_Gen.parameters(), lr=lrG, betas=(0.5,0.999))

BCEloss = nn.BCELoss()

def KL_loss(mu, logvar):
    # -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD_element = mu.pow(2).add_(logvar.exp()).mul_(-1).add_(1).add_(logvar)
    KLD = torch.mean(KLD_element).mul_(-0.5)
    return KLD

def train_StageI_Dis(real_images, wrong_images, text, optimizer):

    optimizer.zero_grad()

    real_images = real_images.to(device)
    text = text.to(device)
    real_pred = StageI_Dis(real_images, text)
    real_targets = torch.ones(real_images.size(0),1)
    real_pred = real_pred.to(device)
    real_targets = real_targets.to(device)
    real_loss = BCEloss(real_pred, real_targets)
    real_score = torch.mean(real_pred).item()

    fake_images, mu, logvar = StageI_Gen(text)
    fake_pred1 = StageI_Dis(fake_images, text)
    fake_targets1 = torch.zeros(fake_images.size(0),1)
    fake_pred1 = fake_pred1.to(device)
    fake_targets1 = fake_targets1.to(device)
    fake_loss1 = BCEloss(fake_pred1, fake_targets1)
    fake_score1 = torch.mean(fake_pred1).item()

    wrong_images = wrong_images.to(device)
    fake_pred2 = StageI_Dis(wrong_images, text)
    fake_targets2 = torch.zeros(wrong_images.size(0),1)
    fake_pred2 = fake_pred2.to(device)
    fake_targets2 = fake_targets2.to(device)
    fake_loss2 = BCEloss(fake_pred2, fake_targets2)
    fake_score2 = torch.mean(fake_pred2).item()

    discriminator_loss = real_loss + (fake_loss1 + fake_loss2)/2
    discriminator_loss.backward()
    optimizer.step()

    return discriminator_loss.item(), real_score, (fake_score1+fake_score2)/2


def train_StageI_Gen(text, optimizer):

    optimizer.zero_grad()

    text = text.to(device)
    generator_images, mu, logvar = StageI_Gen(text)
    generator_pred = StageI_Dis(generator_images, text)
    generator_targets = torch.ones(batch_size, 1)
    generator_pred = generator_pred.to(device)
    generator_targets = generator_targets.to(device)
    gen_bin_loss = BCEloss(generator_pred, generator_targets)
    generator_score = torch.mean(generator_pred).item()
    kl_loss = KL_loss(mu, logvar)

    generator_loss = gen_bin_loss + 2*kl_loss
    generator_loss.backward()
    optimizer.step()

    return generator_loss.item(), gen_bin_loss, kl_loss, generator_score

def save_samples(index1, text, show=True):
    fake_images, a, b = StageI_Gen(text)
    fake_images = fake_images[0:16,:,:,:]
    fake_fname = 'generated-images-{}.png'.format(index1)
    save_image((fake_images), os.path.join("/content/drive/MyDrive/GAN Images/Birds/birds-5", fake_fname), nrow=4)
    if show:
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xticks([]); ax.set_yticks([])
        ax.imshow(make_grid(fake_images.cpu().detach(), nrow=8).permute(1, 2, 0))

''' Stage1 Training'''

def train_StackGAN_StageI(dataset, optimizerD1, optimizerG1, device):

    train_D1Loss_batch = []
    train_G1Loss_batch = []
    train_real_score = []
    train_fake_score = []
    train_generator_score = []

    for idx,(real_images, text) in enumerate(dataset):

        '''If you want to use HuggingFace Sentence Transformer'''
        text = list(text)
        embedding = []
        for i in range(len(text)):
            my_file = open(text[i], "r")
            content = my_file.read()
            embedding.append(content)
        emb = sbert_model.encode(embedding)
        emb = torch.from_numpy(emb)

        wrong_images = torch.flip(real_images, [0])
        discriminator_loss, real_score, fake_score = train_StageI_Dis(real_images, wrong_images, emb, optimizerD1)
        generator_loss, a, b, generator_score = train_StageI_Gen(emb, optimizerG1)
        train_D1Loss_batch.append(discriminator_loss)
        train_G1Loss_batch.append(generator_loss)
        train_real_score.append(real_score)
        train_fake_score.append(fake_score)
        train_generator_score.append(generator_score)

        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
        torch.cuda.empty_cache()
        gc.collect()

    epoch_D1losses.append(sum(train_D1Loss_batch)/len(dataset))
    epoch_G1losses.append(sum(train_G1Loss_batch)/len(dataset))
    epoch_Real_Score.append(sum(train_real_score)/len(dataset))
    epoch_Fake_Score.append(sum(train_fake_score)/len(dataset))
    epoch_Generator_Score.append(sum(train_generator_score)/len(dataset))

    print(f"Discriminator Epoch Loss: {epoch_D1losses[-1]:.5f}   Generator Epoch Loss: {epoch_G1losses[-1]:.5f}   Real Score: {epoch_Real_Score[-1]:.5f}   Fake Score: {epoch_Fake_Score[-1]:.5f}   Generator Score: {epoch_Generator_Score[-1]:.5f}")

    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.empty_cache()
    gc.collect()


