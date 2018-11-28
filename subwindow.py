#!/usr/bin/env python
# coding:utf-8

import tkinter as tk
from PIL import Image, ImageTk

class Promotion:
    def __init__(self, master=None):
        super().__init__()
        master.title("Choice what to Promote")
        master.geometry("+100+40")
        self._openImage()

    
    def _openImage(self):
        self.file = []
        for i in range(12):
            image = Image.open("image/chess"+str(i)+".png")
            self.file.append(ImageTk.PhotoImage(image))
