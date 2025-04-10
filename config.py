import os

from keras_applications import imagenet_utils

args = {
    'im_size': 256,
    'batch_size': 32,
    'num_channels': 3,
    'malnet_tiny': True,
    'group': 'type',  # options: binary, type, family
    'color_mode': 'rgb',  # options: rgb, grayscale

    'epochs': 50,
    'model': 'resnet50',
    'alpha': 1.0,  # sets MobileNet model size
    'weights': 'imagenet',  # options: None (which is random), imagenet
    'loss': 'categorical_crossentropy',  # options: categorical_crossentropy, categorical_focal_loss
    'reweight': None,  # options: None, effective_num
    'reweight_beta': 0.999,  # used if 'reweight' is set to effective_num

    'seed': 1,
    'devices': [0],
    'data_dir': '/teamspace/uploads/malnet-images-tiny01/',  # /teamspace/uploads/malnet-images-tiny01/test  symbolic link directory
    'image_dir': '/teamspace/uploads/malnet-images-tiny01',  # path where data is located

}
