#!/bin/zsh

import sys
import os
import glob
from fastai.vision import *
import argparse
import json
import yaml

dirs = ['data', 'library', 'candidates']
[os.makedirs(d) for d in dirs if not os.path.exists(d)]

# Parse arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dry-run', action='store_true',
                    help='runs drily, iow without actually (re)moving any images')
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
images = glob.glob('./library/*/*.jpg')

RUN_DRILY = args.dry_run

candidates_file_path = 'candidates.yml'
if os.path.isfile(candidates_file_path):
    candidates = yaml.load(open(candidates_file_path), Loader=yaml.FullLoader)

    print(f"Loaded {len(candidates)} candidates")
else:
    candidates = []

# For each image, predict if it's good or bad.
for image_path in images:
    # Get image metadata.
    user_dir = os.path.dirname(image_path)
    user = os.path.split(user_dir)[-1]
    metadata_file_path = f"{user_dir}/{user}.json"
    if os.path.isfile(metadata_file_path):
        with open(metadata_file_path) as f:
            d = json.load(f)
            graph_images = d['GraphImages']
            image_name = os.path.split(image_path)[-1]
            image_metadata_matches = [
                g for g in graph_images if image_name in g['display_url']]
    else:
        print(f"Couldn't find metadata file at {metadata_file_path}!")

    # Check if image should be discarded based on its description.
    if image_metadata_matches:
        image_metadata = image_metadata_matches[0]
        edges = image_metadata['edge_media_to_caption']['edges']
        if edges:
            caption = edges[0]['node']['text']
            if any(x in caption for x in ['link in', 'buy', 'limited', '$', '€', '£']):
                if args.verbose:
                    print(
                        f"Ignored photo {image_path} because of suspected ad.")

                continue
            elif any(x in caption for x in [': @', 'by @', '📸 @', '📷 @']):
                if args.verbose:
                    print(
                        f"Ignored photo {image_path} because of suspected repost.")

                continue

    # Load image and make prediction.
    img = open_image(image_path)
    pred = learn.predict(img)

    # If it's good (with 95% or more confidence), move it to /candidates.
    score = pred[2][1]
    if score > .95:
        print(f"{image_path} is good! (score {score})")

        filename = os.path.split(image_path)[-1]

        if not RUN_DRILY:
            new_path = os.path.join('./candidates', filename)
            os.rename(image_path, new_path)

        # Also, save a record of file path, user name, score and was_posted.
        candidates.append([filename, user, score.item(), False])

    # Otherwise, delete it.
    else:
        if not RUN_DRILY:
            os.remove(image_path)

# Store candidates data to csv file.
if not RUN_DRILY:
    yaml.dump(candidates, open(candidates_file_path, 'w'))

# Clean up remaining files and folders.
if not RUN_DRILY:
    for file in glob.glob('./library/*/*'):
        os.remove(file)

    for folder in glob.glob('./library/*'):
        os.rmdir(folder)
