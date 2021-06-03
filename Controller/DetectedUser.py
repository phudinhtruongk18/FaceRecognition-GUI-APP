import time
from tkinter import ttk, messagebox
import tkinter as jra
from PIL import ImageTk, Image


class DetectedUser:
    def __init__(self, master_temp, menuUI):
        self.menuUI = menuUI
        self.master = master_temp
        # self.master.resizable(1, 1)

        self.master.title("Detected User")
        w, h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()

        # w = 1920
        # hCanvas = 1060
        hCanvas = h - 27
        self.master.geometry("{0}x{1}+0+0".format(w, hCanvas))

        style = ttk.Style()
        self.font = ('Helvetica', 26, "bold")
        style.configure('W.TButton', font=self.font, bg="#faf3e0", fg="#263942")

        self.ROOT_FRAME = ttk.Frame(self.master, height=hCanvas, style="W.TButton")
        self.ROOT_FRAME.grid(row=0, column=0)
        self.right_frame = ttk.Frame(self.ROOT_FRAME)
        self.right_frame.grid(row=0, column=1, sticky=jra.N)
        self.camera_real_time = jra.Canvas(self.right_frame, width=int(w / 3), height=int(h * 6 / 10), bg="#faf3e0")
        self.camera_real_time.grid(row=0, column=0)

        self.canvas_the_packer = jra.Canvas(self.right_frame)
        self.canvas_the_packer.grid(row=1, column=0)
        self.time_left_label = ttk.Label(self.canvas_the_packer, text="Time Left : ", style="W.TButton", width=17)
        self.time_left_label.grid(row=0, column=0)
        self.time_left = ttk.Button(self.canvas_the_packer, style="W.TButton", width=15)
        self.time_left.grid(row=0, column=1)

        self.num_detected_label = ttk.Label(self.canvas_the_packer, text="Detected Employee", style="W.TButton",
                                            width=17)
        self.num_detected_label.grid(row=1, column=0)
        self.num_detected = ttk.Button(self.canvas_the_packer, style="W.TButton", width=15)
        self.num_detected.grid(row=1, column=1)

        self.employee_left_label = ttk.Label(self.canvas_the_packer, text="Employee left", style="W.TButton", width=17)
        self.employee_left_label.grid(row=2, column=0)
        self.employee_left = ttk.Button(self.canvas_the_packer, style="W.TButton", width=15)
        self.employee_left.grid(row=2, column=1)

        self.backup_button = jra.Button(self.right_frame, text="Backup Button", width=30, height=1)
        self.backup_button.configure(bg="#eabf9f", font=self.font, command=self.open_backup_plan)
        self.backup_button.grid(row=4, column=0)
        self.exit_button = jra.Button(self.right_frame, text="Stop session", width=30, height=1)
        self.exit_button.configure(bg="#eabf9f", font=self.font, command=self.stop_detect)
        self.exit_button.grid(row=5, column=0)

        self.left_frame = jra.Frame(self.ROOT_FRAME)
        self.left_frame.grid(row=0, column=2)
        self.canvas = jra.Canvas(self.left_frame, width=int(w * 6.5 / 10), height=hCanvas - 50, bg="#faf3e0")
        # self.canvas = jra.Canvas(self.left_frame)
        self.canvas.pack(side=jra.LEFT, fill=jra.BOTH, expand=1)
        self.scroll_bar = ttk.Scrollbar(self.left_frame, orient=jra.VERTICAL, command=self.canvas.yview)
        self.scroll_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)
        self.secondFrame = jra.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.secondFrame, anchor="nw")
        self.secondFrame.bind('<Configure>', self.on_configure)
        self.list_buttons = []
        self.list_images = []
        self.list_labels = []

        self.row = 0
        self.column = 0
        self.image = ImageTk.PhotoImage(Image.open("View/Stock/homepagepic.png").resize((600, 600), Image.ANTIALIAS))
        self.camera_real_time.create_image(0, 0, anchor=jra.NW, image=self.image)

        self.scroll_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.master.withdraw()

        self.timeBegin = 0
        self.timer_second = 0
        self.button_size = 300

    def backup_plan(self, id_to_backup, backup_box_temp):
        # Get text from this small backup box and do some research in some list and backup them by the ID user input
        # isRecorded = false and Index if employee ID non attendance yet
        # isRecorded = true and id_name if employee ID attendance already
        # None and None if ID doesn't exist in system
        id_to_backup = str(id_to_backup)
        isRecorded, IDorName = self.menuUI.detected_user_from_detector(id_to_backup)
        if isRecorded is None:
            messagebox.showinfo(" Try Again!", "Your ID" + id_to_backup + " doesn't exist!")
        else:
            if isRecorded:
                self.menuUI.backup_detected_user_with_id_to_detector(IDorName)
                # messagebox.showinfo(id_to_backup + " da den!", "Your ID look old!")
            if not isRecorded:
                self.menuUI.backup_detected_user_with_index_to_detector(IDorName)
                # messagebox.showinfo(id_to_backup + " chua den!", "Your ID look new!")
        backup_box_temp.destroy()

    # Get input ID from user and do self.backup_plan()
    def open_backup_plan(self):
        backup_box = jra.Toplevel(self.master)
        backup_box.title("Backup Box")
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 445
        h = 160
        x, y = ws / 2 - w / 2, hs / 2 - h - 50
        backup_box.geometry('%dx%d+%d+%d' % (w, h, x, y))
        backup_id_entry = jra.Entry(backup_box, bg="#faf3e0", font=self.font, justify='center', width=23)
        backup_id_entry.grid(row=0, column=0, sticky="N", ipady=20)
        packet_label = jra.Label(backup_box, bg="#faf3e0")
        confirm_button = jra.Button(packet_label, text="Confirm", bg="#eabf9f", width=10, height=1, font=self.font,
                                    command=lambda: self.backup_plan(backup_id_entry.get(), backup_box))
        confirm_button.grid(row=0, column=0, sticky="SW")
        cancel_button = jra.Button(packet_label, text="Cancel", bg="#eabf9f", width=10, height=1, font=self.font,
                                   command=backup_box.destroy)
        cancel_button.grid(row=0, column=1, sticky="SE")
        packet_label.grid(row=1, column=0, sticky="S")
        backup_id_entry.focus_set()
        backup_id_entry.bind('<Return>', lambda event: self.backup_plan(backup_id_entry.get(), backup_box))

    def update_clock(self):
        # simple time counter update after every second
        now = time.perf_counter()
        time_left = int(self.timer_second - (now - self.timeBegin))
        self.time_left.configure(text=time_left)
        self.master.after(1000, self.update_clock)
        if time_left < 0:
            self.stop_detect()

    def update_detected_text(self, num_of_list, num_of_left):
        # num_of_left += 1
        self.num_detected.configure(text=num_of_list - num_of_left)
        self.employee_left.configure(text=num_of_left)

    def update_image(self, frame):
        # Get the latest frame and convert image format
        # change to PIL format by Image from array first and then change to ImageTk format
        self.image = ImageTk.PhotoImage(Image.fromarray(frame))
        # Update image
        try:
            self.camera_real_time.create_image(0, 0, anchor=jra.NW, image=self.image)
        except Exception as e:
            print("Update Realtime fail ", e)

    def stop_detect(self):
        # stop detecting in Detector
        self.menuUI.stop_detect()
        # hide this window
        self.master.withdraw()
        # reset for new session
        self.reset_data()
        # show up menuUI
        self.menuUI.controller.deiconify()

    def reset_data(self):
        # Un grid all image of old session
        for temp_button in self.list_buttons:
            temp_button.grid_forget()
        for temp_label in self.list_labels:
            temp_label.grid_forget()
        # Clear 2 old lists
        self.list_labels.clear()
        self.list_buttons.clear()
        self.list_images.clear()
        # Set row and column 0 for new record session
        self.row = 0
        self.column = 0

    def show(self, timer):
        # minutes to seconds
        self.timer_second = timer * 60
        self.timeBegin = time.perf_counter()
        # show this window
        self.master.deiconify()
        # start counting down
        self.update_clock()

    def on_configure(self, _):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(-1 * int((event.delta / 150)), "units")

    def get_right_size(self, wi, he):
        ratio = wi / he
        if ratio > 0:
            he, wi = self.button_size, self.button_size * ratio
        else:
            wi, he = self.button_size, self.button_size * ratio
        return int(wi), int(he)

    def add_detected_user(self, user_id):
        # get employee photo
        link_user = "View/Detected/" + user_id + ".jpg"
        user_pic = Image.open(link_user)
        # get right size of user picture and resize to make it good looking and fit to the button
        img = ImageTk.PhotoImage(user_pic.resize(self.get_right_size(user_pic.width, user_pic.height), Image.ANTIALIAS))
        # add to self.list_images -> make it visible (I have tried make it simpler but it doesn't work)
        self.list_images.append(img)
        # do some math to grid in this window
        index = self.list_images.__len__() - 1

        button = jra.Button(self.secondFrame, image=self.list_images[index], width=300, height=300, bg="#faf3e0")
        label = jra.Label(self.secondFrame, text=user_id, bg="#faf3e0", font=self.font)
        if self.column == 4:
            self.column = 0
            self.row += 2
        self.column += 1
        button.bind('<Enter>', lambda event_temp: self.on_start_hover(_=event_temp,
                                                                      button_temp=button, user_id_temp=user_id,
                                                                      label_temp=label))
        button.bind('<Leave>', lambda event_temp: self.on_end_hover(_=event_temp, user_id_temp=user_id,
                                                                    button_temp=button, label_temp=label))
        button.grid(row=self.row, column=self.column)
        label.grid(row=self.row + 1, column=self.column)

        # add to list_buttons -> take control this button
        self.list_buttons.append(button)
        self.list_labels.append(label)

    def on_start_hover(self, _, user_id_temp, button_temp, label_temp):
        button_temp.configure(bg="pink")
        print(self.font)
        label_temp.configure(text="SHOW DETAIL INFORMATION\nabout home and life")

    def on_end_hover(self, _, user_id_temp, button_temp, label_temp):
        if self.list_buttons:
            button_temp.configure(bg="#faf3e0")
            label_temp.configure(text=user_id_temp)
