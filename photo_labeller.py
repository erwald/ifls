#!/bin/zsh

import glob
import random
import tkinter
from PIL import ImageTk, Image
import sys
import os

dirs = ['images', 'data']
[os.makedirs(d) for d in dirs if not os.path.exists(d)]

images = glob.glob('./images/*/*.jpg')
stop = False

root = tkinter.Tk()

image_path = None
image_panel = tkinter.Label(root, image=None)
image_panel.pack(side="bottom", fill="both", expand="yes")


def show_next_image():
    # Pick image.
    global image_path
    image_path = random.choice(images)
    images.remove(image_path)

    # Show image.
    img = ImageTk.PhotoImage(Image.open(image_path))
    image_panel.configure(image=img)
    image_panel.image = img


def close(_arg):
    print('Good-bye!')
    sys.exit()


def good(_arg):
    print(f"Good: {image_path}")
    filename = os.path.split(image_path)[-1]
    good_path = os.path.join('./data/good', filename)
    os.rename(image_path, good_path)
    show_next_image()


def bad(_arg):
    print(f"Bad: {image_path}")
    filename = os.path.split(image_path)[-1]
    bad_path = os.path.join('./data/bad', filename)
    os.rename(image_path, bad_path)
    show_next_image()


root.bind("<Escape>", close)
root.bind("<Right>", good)
root.bind("<Left>", bad)

show_next_image()

root.mainloop()
