import torch
import torch.nn as nn
import torchvision
import numpy as np
import torch.nn.functional as F
import math
from torch.autograd import Variable
import torch.utils.model_zoo as model_zoo
from UNet_zoo.model import *
from UNet_zoo.train import *
from UNetPP_zoo.model import *
from UNetPP_zoo.train import *
from PointNet_zoo.model import *
from PointNet_zoo.train import *
from StackGAN_zoo.model import *
from StackGAN_zoo.train1 import *
from StackGAN_zoo.train2 import *
from CharCNN_zoo.model import *
from PSPNet_zoo.model import *
from PSPNet_zoo.train import *
from Inpainting_zoo.model import *
from Inpainting_zoo.train import *
from AdapAttnIC_zoo.model import *

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
def models(name = None):
    if name is None:
        return "No Models loaded"
    else:
        return f"{name} model loaded successfully"

class UNet:
    def model(num_channels = 1, pretrained = False):
        if pretrained == True:
            model = U_Net(num_channels)
            url = 'https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/U-Net_Image_Seg_Norm.pt'
            checkpoint = model_zoo.load_url(url, map_location=device)
            model.load_state_dict(checkpoint['model_state_dict'])
            print("Pre-Trained Model Loaded Succesfully")
        else:
            model = U_Net(num_channels)
            print("Model Loaded Succesfully") 
        return model
    
    def train(model, train_dataloader, optimizer, loss, device):
        train_UNet(model, train_dataloader, optimizer, loss, device)
    
    def val(model, val_dataloader, loss, device):
        eval_UNet(model, val_dataloader, loss, device)

class UNetPP:
    def model(num_channels = 1, pretrained = False):
        if pretrained == True:
            model = UNet_PP(num_channels = num_channels, denseblock = DenseBlock, basicdownblock = BasicDownBlock, basicupblock = BasicUpBlock)
            url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/U-Net++.pt"    
            checkpoint = model_zoo.load_url(url, map_location=device)
            model.load_state_dict(checkpoint['model_state_dict'])
            print("Pre-Trained Model Loaded Succesfully")
        else:    
            model = UNet_PP(num_channels, DenseBlock, BasicDownBlock, BasicUpBlock)
            print("Model Loaded Succesfully") 
        return model
    
    def train(model, train_dataloader, optimizer, loss, device):
        train_UNetPP(model, train_dataloader, optimizer, loss, device)
    
    def val(model, val_dataloader, loss, device):
        eval_UNetPP(model, val_dataloader, loss, device)

class PointNet:
    def model(pretrained = False):
        if pretrained == True:
            model = Point_Net(T_Net)
            url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/PointNet_Best.pt"
            checkpoint = model_zoo.load_url(url, map_location=device)
            model.load_state_dict(checkpoint['model_state_dict'])
            print("Pre-Trained Model Loaded Succesfully")
        else:
            model = Point_Net(T_Net)
            model = model.apply(weights_init)
            print("Model Loaded Succesfully") 
        return model
    
    def train(model, train_dataloader, optimizer, device):
        train_PointNet(model, train_dataloader, optimizer, device)
    
    def val(model, val_dataloader, device):
        val_PointNet(model, val_dataloader, device)

class CharCNN:
    def model(pretrained = False):
        if pretrained == True:
            model = Char_CNN()
            print("Pre-Trained Model Loaded Succesfully") 
            return model
        else:
            model = Char_CNN()
            print("Model Loaded Succesfully") 
            return model

class StackGAN:
    def model(name = "None", pretrained = False):
        if pretrained == True:
            if name == "None":
                return "Please specify the name of Model"
            elif name == 'StageI_Gen':
                model = StageI_GAN_Gen(Conditioning_Augmentation_StageI)
                url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageI_Gen_GAN_GPT2-3.pt"
                checkpoint = model_zoo.load_url(url, map_location=device)
                model.load_state_dict(checkpoint['model_state_dict'])
                print("Pre-Trained Model Loaded Succesfully")
                return model
            elif name == 'StageI_Dis':
                model = StageI_GAN_Dis(DownSample1)
                url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageI_Dis_GAN_GPT2.pt"
                checkpoint = model_zoo.load_url(url, map_location=device)
                model.load_state_dict(checkpoint['model_state_dict'])
                print("Pre-Trained Model Loaded Succesfully")
                return model
            elif name == 'StageII_Gen':
                model = StageII_GAN_Gen(DownSample2, ResidualBlock, UpSampling2, Conditioning_Augmentation_StageII)
                url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageII_Gen_GAN_GPT2.pt"
                checkpoint = model_zoo.load_url(url, map_location=device)
                model.load_state_dict(checkpoint['model_state_dict'])
                print("Pre-Trained Model Loaded Succesfully")
                return model
            elif name == 'StageII_Dis':
                model = StageII_GAN_Dis(DownSample3)
                url = "https://github.com/Vinayak-VG/ModelZoo_PyPi/releases/download/Weights/StageII_Dis_GAN_GPT2.pt"
                checkpoint = model_zoo.load_url(url, map_location=device)
                model.load_state_dict(checkpoint['model_state_dict'])
                print("Pre-Trained Model Loaded Succesfully")
                return model
        else:
            if name == "None":
                return "Please specify the name of Model"
            elif name == 'StageI_Gen':
                model = StageI_GAN_Gen(Conditioning_Augmentation_StageI)
                model = model.apply(weights_init)
                print("Model Loaded Succesfully") 
                return model
            elif name == 'StageI_Dis':
                model = StageI_GAN_Dis(DownSample1)
                model = model.apply(weights_init)
                print("Model Loaded Succesfully") 
                return model
            elif name == 'StageII_Gen':
                model = StageII_GAN_Gen(DownSample2, ResidualBlock, UpSampling2, Conditioning_Augmentation_StageII)
                model = model.apply(weights_init)
                print("Model Loaded Succesfully") 
                return model
            elif name == 'StageII_Dis':
                model = StageII_GAN_Dis(DownSample3)
                model = model.apply(weights_init)
                print("Model Loaded Succesfully") 
                return model

    def trainI(dataset, optimizerD1, optimizerG1, device):
        train_StackGAN_StageI(dataset, optimizerD1, optimizerG1, device)

    def trainII(dataset, optimizerD1, optimizerG1, device):
        train_StackGAN_StageII(dataset, optimizerD1, optimizerG1, device)

class Inpainting:
    def model(name = "None", pretrained = False):
        if pretrained == True:
            if name == "None":
                return "Please specify the name of Model"
            elif name == 'Generator':
                model = Generator(use_cuda=True)
                print("Pre-Trained Model Loaded Succesfully")
                return model
            elif name == 'LocalDis':
                model = LocalDis()
                print("Pre-Trained Model Loaded Succesfully")
                return model
            elif name == 'GlobalDis':
                model = GlobalDis()
                print("Pre-Trained Model Loaded Succesfully")
                return model
        else:
            if name == "None":
                return "Please specify the name of Model"
            elif name == 'Generator':
                model = Generator(use_cuda=True)
                print("Model Loaded Succesfully") 
                return model
            elif name == 'LocalDis':
                model = LocalDis()
                print("Model Loaded Succesfully") 
                return model
            elif name == 'GlobalDis':
                model = GlobalDis()
                print("Model Loaded Succesfully") 
                return model

    def train(net_gen, net_local_dis, net_global_dis, dataset, optimizer_g, optimizer_d, criterionL1):
        train_Inpainting(net_gen, net_local_dis, net_global_dis, dataset, optimizer_g, optimizer_d, criterionL1)

    def val(net_gen, dataset,criterionL1):
        val_Inpainting(net_gen, dataset,criterionL1)

class PSPNet:
    def model(pretrained = False):
        if pretrained == True:
            model = PSP_Net()
            print("Pre-Trained Model Loaded Succesfully") 
            return model
        else: 
            model = PSP_Net()
            print("Model Loaded Succesfully") 
            return model

    def train(model, dataset, optimizer, epoch, device):
        train_PSPNet(model, dataset, optimizer, epoch, device)
    
    def val(model, dataset, epoch, device):
        val_PSPNet(model, dataset, epoch, device)

class AdapAttnIC:
    def model(embed_dim, hidden_dim, feature_dim, vocab_size, weights_matrix, name = 'None',pretrained = False):
        if pretrained == True:
            if name == "None":
                return "Please specify the name of Model"
            elif name == 'Encoder':
                model = Encoder()
                print("Pre-Trained Model Loaded Succesfully")
                return model
            elif name == 'Decoder':
                model = Decoder(embed_dim, hidden_dim, feature_dim, vocab_size, weights_matrix, device)
                print("Pre-Trained Model Loaded Succesfully")
                return model
        if pretrained == False:
            if name == "None":
                return "Please specify the name of Model"
            elif name == 'Encoder':
                model = Encoder()
                print("Model Loaded Succesfully") 
                return model
            elif name == 'Decoder':
                model = Decoder(embed_dim, hidden_dim, feature_dim, vocab_size, weights_matrix, device)
                print("Model Loaded Succesfully") 
                return model



