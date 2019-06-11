import sys
import os
import glob
from sklearn.model_selection import train_test_split

# Takes all the data we've labelled thus far, splits it into a train and a
# validation set, and moves it into the appropriate folders.

good_images = glob.glob('./data/good/*.jpg')
bad_images = glob.glob('./data/bad/*.jpg')

valid_size = 0.15
good_train, good_valid = train_test_split(good_images, test_size=valid_size)
bad_train, bad_valid = train_test_split(bad_images, test_size=valid_size)


def move_files(image_paths, base_path):
    for image_path in image_paths:
        filename = os.path.split(image_path)[-1]
        new_path = os.path.join(base_path, filename)
        os.rename(image_path, new_path)


move_files(good_train, './data/train/good')
move_files(good_valid, './data/valid/good')
move_files(bad_train, './data/train/bad')
move_files(bad_valid, './data/valid/bad')
