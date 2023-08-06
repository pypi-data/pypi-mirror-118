import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
import torch.optim as optim
from torch.utils.data import DataLoader
from torch import autograd
import gc

import time
import pyprind

import matplotlib.pyplot as plt

from Inpainting_zoo.model import *
from Inpainting_zoo.loss import *
from Inpainting_zoo.utilities import *

### Parameters ###

batch_size = 6
start_epochs = 0
total_epochs = 8 
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

### Initializing the Model ###

net_gen = Generator(use_cuda=True)
net_local_dis = LocalDis()
net_global_dis = GlobalDis()

net_gen.to(device)
net_local_dis.to(device)
net_global_dis.to(device)

d_params = list(net_local_dis.parameters()) + list(net_global_dis.parameters())
optimizer_g = optim.Adam(net_gen.parameters(), lr=0.0001, betas=(0.5, 0.9))
optimizer_d = optim.Adam(d_params, lr=0.0001, betas=(0.5, 0.9))

criterionL1 = nn.L1Loss().to(device)

### Train Functions ###

def dis_forward(netD, ground_truth, x_inpaint):
    #assert ground_truth.size() == x_inpaint.size()
    batch_size = ground_truth.size(0)
    batch_data = torch.cat([ground_truth, x_inpaint], dim=0)
    batch_output = netD(batch_data.float())
    real_pred, fake_pred = torch.split(batch_output, batch_size, dim=0)

    return real_pred, fake_pred

def train_Inpainting(net_gen, net_local_dis, net_global_dis, dataset, optimizer_g, optimizer_d, criterionL1):

    epoch_loss = {'l1':0, 'ae':0, 'wgan_g':0, 'wgan_d':0, 'wgan_gp':0, 'g':0, 'd':0}
    train_loss = []

    epoch_start = time.time()
    gc.collect()
    torch.cuda.empty_cache()

    net_gen.train()
    net_local_dis.train()
    net_global_dis.train()

    bar = pyprind.ProgBar(len(dataset), bar_char='█')
    for idx, ground_truth in enumerate(dataset, 1):

        gc.collect()
        torch.cuda.empty_cache()

        batch_size = ground_truth.size(0)
        bboxes = random_bbox(batch_size=batch_size)
        x, mask = mask_image(ground_truth, bboxes)

        ground_truth = ground_truth.to(device)
        x = x.to(device)
        mask = mask.to(device)

        losses = {}

        ##################
        ### Prediction ###
        ##################

        x1, x2, offset_flow = net_gen(x.float(), mask)
        local_patch_gt = local_patch(ground_truth, bboxes)
        x1_inpaint = x1 * mask + x * (1. - mask)
        x2_inpaint = x2 * mask + x * (1. - mask)
        local_patch_x1_inpaint = local_patch(x1_inpaint, bboxes)
        local_patch_x2_inpaint = local_patch(x2_inpaint, bboxes)

        gc.collect()
        torch.cuda.empty_cache()

        ##########################
        ### Discriminator Loss ###
        ##########################

        ### Local Discriminator ###
                                                    
        local_patch_real_pred, local_patch_fake_pred = dis_forward(net_local_dis, local_patch_gt, local_patch_x2_inpaint.detach())

        gc.collect()
        torch.cuda.empty_cache()

        ### Global Discriminator ###

        global_real_pred, global_fake_pred = dis_forward(net_global_dis, ground_truth, x2_inpaint.detach())

        gc.collect()
        torch.cuda.empty_cache()

        ### Computing Losses ###

        losses['wgan_d'] = torch.mean(local_patch_fake_pred-local_patch_real_pred) + torch.mean(global_fake_pred-global_real_pred)
        
        local_penalty = calc_gradient_penalty(net_local_dis, local_patch_gt, local_patch_x2_inpaint.detach(), device)
        global_penalty = calc_gradient_penalty(net_global_dis, ground_truth, x2_inpaint.detach(), device)
        losses['wgan_gp'] = local_penalty + global_penalty

        gc.collect()
        torch.cuda.empty_cache()

        ######################
        ### Generator Loss ###
        ######################

        sd_mask = spatial_discounting_mask(use_cuda=True)

        losses['l1'] = 1.2*criterionL1(local_patch_x1_inpaint*sd_mask, local_patch_gt*sd_mask) + criterionL1(local_patch_x2_inpaint*sd_mask, local_patch_gt*sd_mask)

        losses['ae'] = 1.2*criterionL1(x1*(1.-mask), ground_truth*(1.-mask)) + criterionL1(x2*(1.-mask), ground_truth*(1.-mask))

        local_patch_real_pred_gen, local_patch_fake_pred_gen = dis_forward(net_local_dis, local_patch_gt, local_patch_x2_inpaint)
        global_real_pred_gen, global_fake_pred_gen = dis_forward(net_global_dis, ground_truth, x2_inpaint)
        losses['wgan_g'] = - torch.mean(local_patch_fake_pred_gen) - torch.mean(global_fake_pred_gen)

        gc.collect()
        torch.cuda.empty_cache()

        ####################
        ### Forward Pass ###
        ####################

        for k in losses.keys():
            if not losses[k].dim() == 0:
                losses[k] = torch.mean(losses[k])

        #####################
        ### Backward Pass ###
        #####################
        with torch.autograd.set_detect_anomaly(True):
            if idx%5 !=0:
                optimizer_d.zero_grad()
                losses['d'] = losses['wgan_d'] + losses['wgan_gp']*10
                losses['d'].backward()
                optimizer_d.step()
            else:
                optimizer_g.zero_grad()
                losses['g'] = losses['l1']*1.2 + losses['ae']*1.2 + losses['wgan_g']*0.001
                losses['g'].backward()
                optimizer_g.step()

        gc.collect()
        torch.cuda.empty_cache()

        #####################
        ### Visualization ###
        #####################

        for key in losses.keys():
            epoch_loss[key] += losses[key].item()/len(dataset)

        #train_loss.append(losses)
        
        bar.update()
        gc.collect()
        torch.cuda.empty_cache()

    gc.collect()
    torch.cuda.empty_cache()

    print(" | Train Loss: Generator: {0}  |  Disctiminator: {1}".format(epoch_loss['g'], epoch_loss['d']))

def val_Inpainting(net_gen, dataset,criterionL1):

    epoch_loss = {'l1':0, 'ae':0, 'wgan_g':0, 'g':0}
    eval_loss = []

    gc.collect()
    torch.cuda.empty_cache()

    net_gen.eval()
    net_local_dis.eval()
    net_global_dis.eval()

    with torch.no_grad():
        bar = pyprind.ProgBar(len(dataset), bar_char='█')
        for idx, ground_truth in enumerate(dataset, 1):

            gc.collect()
            torch.cuda.empty_cache()

            batch_size = ground_truth.size(0)
            bboxes = random_bbox(batch_size=batch_size)
            x, mask = mask_image(ground_truth, bboxes)

            ground_truth = ground_truth.to(device)
            x = x.to(device)
            mask = mask.to(device)

            losses = {}

            ##################
            ### Prediction ###
            ##################

            x1, x2, offset_flow = net_gen(x.float(), mask)
            local_patch_gt = local_patch(ground_truth, bboxes)
            x1_inpaint = x1 * mask + x * (1. - mask)
            x2_inpaint = x2 * mask + x * (1. - mask)
            local_patch_x1_inpaint = local_patch(x1_inpaint, bboxes)
            local_patch_x2_inpaint = local_patch(x2_inpaint, bboxes)

            gc.collect()
            torch.cuda.empty_cache()

            ######################
            ### Generator Loss ###
            ######################

            sd_mask = spatial_discounting_mask(use_cuda=True)

            losses['l1'] = 1.2*criterionL1(local_patch_x1_inpaint*sd_mask, local_patch_gt*sd_mask) + criterionL1(local_patch_x2_inpaint*sd_mask, local_patch_gt*sd_mask)

            losses['ae'] = 1.2*criterionL1(x1*(1.-mask), ground_truth*(1.-mask)) + criterionL1(x2*(1.-mask), ground_truth*(1.-mask))

            local_patch_real_pred, local_patch_fake_pred = dis_forward(net_local_dis, local_patch_gt, local_patch_x2_inpaint)
            global_real_pred, global_fake_pred = dis_forward(net_global_dis, ground_truth, x2_inpaint)
            losses['wgan_g'] = - torch.mean(local_patch_fake_pred) - torch.mean(global_fake_pred)

            gc.collect()
            torch.cuda.empty_cache()

            ####################
            ### Forward Pass ###
            ####################

            losses['g'] = losses['l1']*1.2 + losses['ae']*1.2 + losses['wgan_g']*0.001
            for k in losses.keys():
                if not losses[k].dim() == 0:
                    losses[k] = torch.mean(losses[k])

            #####################
            ### Visualization ###
            #####################

            for key in losses.keys():
                epoch_loss[key] += losses[key].item()/len(dataset)

            #eval_loss.append(losses)
            
            bar.update()
            gc.collect()
            torch.cuda.empty_cache()

    gc.collect()
    torch.cuda.empty_cache()
    print(" | Validation Loss: Generator: {0}".format(epoch_loss['g']))


### Training ###

train_loss = []
val_loss = []

# for epoch in range(start_epochs+1, total_epochs+start_epochs+1):
#     print("Starting Epoch[{0}/{1}]".format(epoch, total_epochs+start_epochs))
    
#     epoch_start = time.time()

#     train_epoch_loss, _ = train(net_gen, net_local_dis, net_global_dis, trainloader, optimizer_g, optimizer_d, criterionL1)
#     train_loss.append(train_epoch_loss)
#     print(" | Train Loss: Generator: {0}  |  Disctiminator: {1}".format(train_epoch_loss['g'], train_epoch_loss['d']))

#     val_epoch_loss, _ = evaluate(net_gen, valloader, criterionL1)
#     val_loss.append(val_epoch_loss)
#     print(" | Validation Loss: Generator: {0}".format(val_epoch_loss['g']))
    

#     epoch_end = time.time()

#     minutes, seconds = epoch_time(epoch_end, epoch_start)

#     print("Finished Epoch[{0}/{1}]".format(epoch, total_epochs+start_epochs))