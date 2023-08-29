import torch
from torchvision import transforms

from torch.utils.data import DataLoader
from torch.utils.data import Dataset as BaseDataset
import torch.optim as optim
import albumentations as albu
from torchvision.transforms import ToTensor

import pytorch_lightning as pl
from pytorch_lightning.callbacks import EarlyStopping
from pytorch_lightning.loggers import TensorBoardLogger

import distutils

import torch.nn.functional as F
import segmentation_models_pytorch as smp

from . model_pytorch import Model

model_path = ".\models_checkpoints\model_checkpoints\version_576\checkpoints\epoch=5-step=521.ckpt"

loss = smp.losses.DiceLoss(smp.losses.constants.MULTICLASS_MODE)
optimizer = optim.Adam
selected_parameters = {'model': 'unetplusplus',
                'encoder_name': 'efficientnet-b2',
                'in_channels': 3, 'classes': 3,
                'encoder_weights': 'imagenet',
                'loss': loss,
                'optimizer': optimizer,
                'learning_rate': 0.0008000076640604941,
                'minimum_learning_rate': 5e-06,
                'scheduler_used': False,
                'decoder_attention_type': None}

class SegmentationModel:
    
    def __init__(self, id):
        self.id = id

        self.model = self.generate_model(info=False, **selected_parameters)
        checkpoint = torch.load("/content/version_576/checkpoints/epoch=5-step=521.ckpt", map_location=torch.device('cpu'))
        self.model.load_state_dict(checkpoint['state_dict'])


    def generate_model(self, info = True, **kwargs):
        arch = kwargs['model']
        encoder_name = kwargs['encoder_name']
        in_channels = kwargs['in_channels']
        classes = kwargs['classes']
        loss = kwargs['loss']
        optimizer = kwargs['optimizer']
        learning_rate = kwargs['learning_rate']
        minimum_learning_rate = kwargs['minimum_learning_rate']
        scheduler_used = kwargs['scheduler_used']

        if info:
            for key, value in kwargs.items():
                print(f"{key}: {value}")

        kwargs = {key: value for key, value in kwargs.items() if value is not None and key != 'model' and key != 'encoder_name' and key != 'in_channels' and key != 'classes'
                and key != 'loss' and key != 'optimizer' and key != 'learning_rate' and key != 'minimum_learning_rate' and key != 'scheduler_used'}

        model = Model(arch, encoder_name, in_channels, classes, loss, optimizer, learning_rate, minimum_learning_rate, scheduler_used, **kwargs)
        # print(model)
        return model

    def to_tensor(self, x, **kwargs):
        return x.astype('float32')

    def get_single_image_preprocessing(self):
        """Construct preprocessing transform

        Args:
            preprocessing_fn (callable): data normalization function
                (can be specific for each pretrained neural network)
        Return:
            transform: albumentations.Compose
        """
        _transform = [
            albu.Lambda(image=self.to_tensor),
        ]
        return albu.Compose(_transform)
