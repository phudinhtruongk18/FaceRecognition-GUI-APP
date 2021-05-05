import os
import textwrap
from tkinter import ttk
import tkinter as jra
from PIL import ImageTk, Image

# from SanPham import SanPham

# linkThuMuc = os.path.abspath(os.getcwd())


class DetectedUser:
    def __init__(self, master_temp):
        self.master = master_temp
        self.master.title("Detected User")
        # master.iconbitmap("logo.ico")
        w = 1980  # width for the Tk root
        h = 450  # height for the Tk root
        ws = master_temp.winfo_screenwidth()  # width of the screen
        hs = master_temp.winfo_screenheight()  # height of the screen
        x = ws/2 - w/2 + 20
        y = (hs / 2) + 20
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.frame_select = jra.Frame(self.master, bg="pink", height=600)
        self.frame_select.grid(row=0, column=1, sticky="nswe")

        self.main_frame = jra.Frame(self.frame_select)
        self.main_frame.grid(row=0, column=2)
        self.canvas = jra.Canvas(self.main_frame, width=w - 90, height=h - 10)
        self.canvas.pack(side=jra.LEFT, fill=jra.BOTH, expand=1)
        self.scrool_bar = ttk.Scrollbar(self.main_frame, orient=jra.VERTICAL, command=self.canvas.yview)
        self.scrool_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.canvas.configure(yscrollcommand=self.scrool_bar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)
        self.secondFrame = jra.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.secondFrame, anchor="nw")

        self.list_buttons = []
        self.list_images = []

        for temp in range(120):
            link_temp = "../View/Stock/user-circle.png"
            img = ImageTk.PhotoImage(Image.open(link_temp).resize((46 * 4, 60 * 4), Image.ANTIALIAS))
            self.list_images.append(img)
        self.row = 0
        self.column = 0
        for temp in range(120):
            button = jra.Button(self.secondFrame, text=temp, image=self.list_images[temp])
            # button.configure(command=lambda btn=button: self.OnClick(btn))
            if self.column == 10:
                self.column = 0
                self.row += 1
            self.column += 1
            self.list_buttons.append(button)
            button.grid(row=self.row, column=self.column)
        self.scrool_bar.pack(side=jra.RIGHT, fill=jra.Y)

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 150)), "units")

