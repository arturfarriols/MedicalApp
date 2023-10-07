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

import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class Model(pl.LightningModule):

    def __init__(self, arch, encoder_name, in_channels, out_classes, loss, optimizer, learning_rate, minimum_learning_rate, scheduler_used, **kwargs):
        super().__init__()
        self.model = smp.create_model(
            arch, encoder_name=encoder_name, in_channels=in_channels, classes=out_classes, **kwargs
        )

        params = smp.encoders.get_preprocessing_params(encoder_name)
        self.register_buffer("std", torch.tensor(params["std"]).view(1, 3, 1, 1))
        self.register_buffer("mean", torch.tensor(params["mean"]).view(1, 3, 1, 1))

        self.loss_fn = loss
        self.chosen_opt = optimizer
        self.learning_rate = learning_rate
        self.minimum_learning_rate = minimum_learning_rate
        self.scheduler_used = scheduler_used


    def forward(self, image):
        # normalize image
        image = (image - self.mean) / self.std
        if image.dim() == 3:
            image = image.unsqueeze(0)  # Add batch dimension if it's missing
        mask = self.model(image)
        return mask

    def shared_step(self, batch, stage):

        global NUMBER_OF_CLASSES

        image = batch[0]

        # Shape of the image should be (batch_size, num_channels, height, width)
        # if you work with grayscale images, expand channels dim to have [batch_size, 1, height, width]
        assert image.ndim == 4

        # Check that image dimensions are divisible by 32,
        # encoder and decoder connected by `skip connections` and usually encoder have 5 stages of
        # downsampling by factor 2 (2 ^ 5 = 32); e.g. if we have image with shape 65x65 we will have
        # following shapes of features in encoder and decoder: 84, 42, 21, 10, 5 -> 5, 10, 20, 40, 80
        # and we will get an error trying to concat these features
        h, w = image.shape[2:]
        assert h % 32 == 0 and w % 32 == 0

        mask = batch[1]
        # print("mask", mask.shape)

        # Shape of the mask should be [batch_size, num_classes, height, width]
        # for binary segmentation num_classes = 1
        assert mask.ndim == 4

        # Check that mask values in between 0 and 1, NOT 0 and 255 for binary segmentation
        # assert mask.max() <= 1.0 and mask.min() >= 0

        logits_mask = self.forward(image)
        # print("logits_mask", logits_mask.shape)

        # Predicted mask contains logits, and loss_fn param `from_logits` is set to True
        loss = self.loss_fn(logits_mask, mask)

        # Lets compute metrics for some threshold
        # first convert mask values to probabilities, then
        # apply thresholding
        print(self.loss_fn.mode )
        if self.loss_fn.mode == "binary":
            prob_mask = logits_mask.sigmoid()
            pred_mask = (prob_mask > 0.5).float()
        elif self.loss_fn.mode == "multiclass":
            prob_mask = logits_mask.softmax(dim=1)
            # print("prob_mask", np.shape(prob_mask))
            # print(torch.unique(prob_mask))
            _, predicted_labels = torch.max(prob_mask, dim=1)

            # Map the predicted labels to the desired class values
            predicted_labels = predicted_labels.to(torch.float32)  # Convert to float for consistency
            predicted_labels = predicted_labels * 2 / (NUMBER_OF_CLASSES - 1)  # Scale the values to range [0, 2]
            # print(torch.unique(predicted_labels))
            predicted_labels = predicted_labels.unsqueeze(dim=1)



        # We will compute IoU metric by two ways
        #   1. dataset-wise
        #   2. image-wise
        # but for now we just compute true positive, false positive, false negative and
        # true negative 'pixels' for each image and class
        # these values will be aggregated in the end of an epoch
        if self.loss_fn.mode == "binary":
            tp, fp, fn, tn = smp.metrics.get_stats(pred_mask.long(), mask.long(), mode="binary")
        elif self.loss_fn.mode == "multiclass":
            tp, fp, fn, tn = smp.metrics.get_stats(predicted_labels.long(), mask.long(), mode="multiclass", num_classes = NUMBER_OF_CLASSES)
        return {
            "loss": loss,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
        }

    def shared_epoch_end(self, outputs, stage):
        # aggregate step metics
        tp = torch.cat([x["tp"] for x in outputs])
        fp = torch.cat([x["fp"] for x in outputs])
        fn = torch.cat([x["fn"] for x in outputs])
        tn = torch.cat([x["tn"] for x in outputs])

        # Calculate the loss
        losses = [x["loss"] for x in outputs]
        loss = torch.stack(losses).mean()


        # per image IoU means that we first calculate IoU score for each image
        # and then compute mean over these scores
        per_image_iou = smp.metrics.iou_score(tp, fp, fn, tn, reduction="micro-imagewise")

        # dataset IoU means that we aggregate intersection and union over whole dataset
        # and then compute IoU score. The difference between dataset_iou and per_image_iou scores
        # in this particular case will not be much, however for dataset
        # with "empty" images (images without target class) a large gap could be observed.
        # Empty images influence a lot on per_image_iou and much less on dataset_iou.
        dataset_iou = smp.metrics.iou_score(tp, fp, fn, tn, reduction="micro")

        metrics = {
            f"{stage}_per_image_iou": per_image_iou,
            f"{stage}_dataset_iou": dataset_iou,
            f"{stage}_loss": loss,
        }

        self.log_dict(metrics, prog_bar=True)

    def training_step(self, batch, batch_idx):
        current_lr = self.trainer.optimizers[0].param_groups[0]['lr']
        print("Learning rate:", current_lr)
        return self.shared_step(batch, "train")

    def training_epoch_end(self, outputs):
        return self.shared_epoch_end(outputs, "train")

    def validation_step(self, batch, batch_idx):
        return self.shared_step(batch, "valid")

    def validation_epoch_end(self, outputs):
        return self.shared_epoch_end(outputs, "valid")

    def test_step(self, batch, batch_idx):
        return self.shared_step(batch, "test")

    def test_epoch_end(self, outputs):
        return self.shared_epoch_end(outputs, "test")


    def configure_optimizers(self):
        optimizer = self.chosen_opt(self.parameters(), self.learning_rate)
        if self.scheduler_used:
            scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
                optimizer, mode='min', factor=0.5, patience=2, verbose=True,
                threshold_mode='abs', threshold=1e-3, cooldown=0, min_lr=self.minimum_learning_rate,
                eps=1e-08
            )
            return {
                'optimizer': optimizer,
                'lr_scheduler': {
                    'scheduler': scheduler,
                    'monitor': 'valid_loss'
                }
            }
        else:
            return optimizer