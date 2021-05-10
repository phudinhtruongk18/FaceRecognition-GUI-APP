from tkinter import ttk
import tkinter as jra
from PIL import ImageTk, Image


class DetectedUser:
    def __init__(self, master_temp):
        self.master = master_temp
        self.master.title("Detected User")
        w = 1920
        hCanvas = 1080
        self.master.geometry("{0}x{1}+0+0".format(w,hCanvas))
        self.ROOT_FRAME = jra.Frame(self.master, bg="#faf3e0", height=hCanvas)
        self.ROOT_FRAME.grid(row=0, column=0)
        self.right_frame = jra.Frame(self.ROOT_FRAME, bg="#faf3e0")
        self.right_frame.grid(row=0, column=1,sticky=jra.N)
        self.camera_real_time = jra.Canvas(self.right_frame, width=640,height=640, bg="#faf3e0")
        self.camera_real_time.grid(row=0, column=0)
        self.time_left = jra.Label(self.right_frame,text="time left", bg="#faf3e0")
        self.time_left.grid(row=1, column=0)
        self.num_detected = jra.Label(self.right_frame,text="num_detected", bg="#faf3e0")
        self.num_detected.grid(row=2, column=0)
        self.num_left = jra.Label(self.right_frame,text="num left", bg="#faf3e0")
        self.num_left.grid(row=3, column=0)
        self.backup_button = jra.Button(self.right_frame,text="backup button", bg="#eabf9f", width=90,height=4)
        self.backup_button.grid(row=4, column=0)
        self.exit_button = jra.Button(self.right_frame,text="exit", bg="#eabf9f", width=90,height=4)
        self.exit_button.grid(row=5, column=0)

        self.left_frame = jra.Frame(self.ROOT_FRAME)
        self.left_frame.grid(row=0, column=2)
        self.canvas = jra.Canvas(self.left_frame, width=1242, height=hCanvas-50, bg="#faf3e0")
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

        self.row = 0
        self.column = 0

        self.scrool_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.master.withdraw()


    def update_image(self,frame):
        # Get the latest frame and convert image format
        # self.image = frame
        print(frame)
        self.image = frame
        self.image = Image.fromarray(self.image)  # to PIL format
        self.image = ImageTk.PhotoImage(self.image)  # to ImageTk format
        # Update image
        self.camera_real_time.create_image(0, 0, anchor=jra.NW, image=self.image)

    def show(self):
        self.master.deiconify()

    def on_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 150)), "units")

    def get_right_size(self,wi,he):
        ratio = wi / he
        if ratio > 0:
            he,wi = 300,300*ratio
        else:
            wi,he = 300,300*ratio
        return int(wi),int(he)

    def add_detected_user(self,user_id):
        link_user = "View/Detected/"+user_id+".jpg"
        user_pic = Image.open(link_user)
        # get right size of user picture and resize to make it look good
        img = ImageTk.PhotoImage(user_pic.resize(self.get_right_size(user_pic.width, user_pic.height), Image.ANTIALIAS))
        self.list_images.append(img)
        index = self.list_images.__len__() - 1
        button = jra.Button(self.secondFrame, image=self.list_images[index], width=300, height=300)
        self.list_buttons.append(button)
        if self.column == 3:
            self.column = 0
            self.row += 1
        self.column += 1
        self.list_buttons.append(button)
        button.grid(row=self.row, column=self.column)
