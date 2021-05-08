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
        w = 980  # width for the Tk root
        h = 550  # height for the Tk root
        ws = master_temp.winfo_screenwidth()  # width of the screen
        hs = master_temp.winfo_screenheight()  # height of the screen
        x = ws/2 - w/2 + 20
        y = (hs / 2) + 20
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # pad = 3
        # self.master.geometry("{0}x{1}+0+0".format(
        #     self.master.winfo_screenwidth() - pad, self.master.winfo_screenheight() - pad))
        self.ROOT_FRAME = jra.Frame(self.master, bg="pink", height=600)
        self.ROOT_FRAME.grid(row=0, column=0, sticky="nswe")
        self.right_frame = jra.Frame(self.ROOT_FRAME)
        self.right_frame.grid(row=0, column=1)
        self.camera_real_time = jra.Canvas(self.right_frame)
        self.camera_real_time.pack()
        self.time_left = jra.Label(self.right_frame,text="time left")
        self.time_left.pack()
        self.num_detected = jra.Label(self.right_frame,text="num_detected")
        self.num_detected.pack()
        self.num_left = jra.Label(self.right_frame,text="num left")
        self.num_left.pack()
        self.backup_button = jra.Button(self.right_frame,text="backup button")
        self.backup_button.pack()
        self.exit_button = jra.Button(self.right_frame,text="exit")
        self.exit_button.pack()

        self.left_frame = jra.Frame(self.ROOT_FRAME)
        self.left_frame.grid(row=0, column=2)
        self.canvas = jra.Canvas(self.left_frame, width=w * 2/3, height=h)
        # self.canvas = jra.Canvas(self.left_frame)
        self.canvas.pack(side=jra.LEFT, fill=jra.BOTH, expand=1)
        self.scrool_bar = ttk.Scrollbar(self.left_frame, orient=jra.VERTICAL, command=self.canvas.yview)
        self.scrool_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.canvas.configure(yscrollcommand=self.scrool_bar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)
        self.secondFrame = jra.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.secondFrame, anchor="nw")
        self.secondFrame.bind('<Configure>', self.on_configure)

        self.list_buttons = []
        self.list_images = []

        # for temp in range(120):
        #     link_temp = "View/Stock/user-circle.png"
        #     img = ImageTk.PhotoImage(Image.open(link_temp).resize((46 * 4, 60 * 4), Image.ANTIALIAS))
        #     self.list_images.append(img)
        self.row = 0
        self.column = 0
        # for temp in range(120):
        #     button = jra.Button(self.secondFrame, text=temp, image=self.list_images[temp])
        #     # button.configure(command=lambda btn=button: self.OnClick(btn))
        #     if self.column == 10:
        #         self.column = 0
        #         self.row += 1
        #     self.column += 1
        #     self.list_buttons.append(button)
        #     button.grid(row=self.row, column=self.column)
        self.scrool_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.master.withdraw()

    def show(self):
        self.master.deiconify()

    def on_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 150)), "units")

    def add_detected_user(self,user_id):
        link_user = "View/Detected/"+user_id+".jpg"
        img = ImageTk.PhotoImage(Image.open(link_user).resize((46 * 8, 60 * 8), Image.ANTIALIAS))
        self.list_images.append(img)
        index = self.list_images.__len__() - 1
        button = jra.Button(self.secondFrame, image=self.list_images[index])
        self.list_buttons.append(button)
        if self.column == 5:
            self.column = 0
            self.row += 1
        self.column += 1
        self.list_buttons.append(button)
        button.grid(row=self.row, column=self.column)
