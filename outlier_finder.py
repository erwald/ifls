#!/bin/zsh

import sys
import os
import glob
from fastai.vision import *
import argparse
import json
import yaml

# Parse arguments.
parser = argparse.ArgumentParser()
parser.add_argument('--check-valid', action='store_true',
                    help='checks the images in the validation set (rather than training set)')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='runs verbosely')
args = parser.parse_args()

# Set up model for classifying.
tfms = get_transforms(max_rotate=None, max_zoom=1.,
                      max_lighting=None, max_warp=None)
data = ImageDataBunch.single_from_classes(
    './data', ['bad', 'good'], ds_tfms=tfms, size=112)

learn = cnn_learner(data, models.resnet50, metrics=[error_rate])
learn.load('model')

# Get paths of all prospective images.
folder = './data/valid/bad/*.jpg' if args.check_valid else './data/train/bad/*.jpg'
images = glob.glob(folder)

# For each image, predict if it's good or bad.
for image_path in images:
    # Load image and make prediction.
    img = open_image(image_path)
    pred = learn.predict(img)

    # If it's good (with 98% or more confidence), log it.
    score = pred[2][1]
    if score > .98:
        print(f"{image_path} is good (score {score})")
