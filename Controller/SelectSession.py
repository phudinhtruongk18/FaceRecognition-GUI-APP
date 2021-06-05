import os
from tkinter import ttk, messagebox
import tkinter as jra
from PIL import ImageTk, Image


class SelectSession:
    def __init__(self, master_temp=None, menuUI=None):
        self.picked_user = []
        self.menuUI = menuUI
        self.master = master_temp

        self.master.title("Select Session")
        w, h = int(self.master.winfo_screenwidth() * 5 / 6) + 50, int(self.master.winfo_screenheight() * 5 / 6)

        hCanvas = h - 27
        self.master.geometry("{0}x{1}+0+0".format(w, hCanvas))

        style = ttk.Style()
        self.font = ('Helvetica', 23, "bold")

        self.ROOT_FRAME = jra.Frame(self.master, height=hCanvas)
        self.ROOT_FRAME.grid(row=0, column=0)
        self.right_frame = ttk.Frame(self.ROOT_FRAME)
        self.right_frame.grid(row=0, column=1, sticky=jra.N)

        self.canvas_the_packer = jra.Canvas(self.right_frame, bg="#0CEDCB")
        self.canvas_the_packer.grid(row=1, column=0)

        self.time_left_label = jra.Label(self.canvas_the_packer, bg="#0CEDCB", text="Select Saved Session   ",
                                         font=('Helvetica', 20, "bold"), width=22)
        self.time_left_label.grid(row=0, column=0, ipady=10)

        self.label_option = ttk.Label(self.canvas_the_packer, style="W.TButton", width=19)
        self.label_option.grid(row=1, column=0)
        self.selected_session = jra.StringVar(self.master, value="Select Your Session")

        self.saved_sesions = self.get_saved_sesion()
        self.session_option = jra.OptionMenu(self.label_option, self.selected_session, *self.saved_sesions)
        self.session_option.configure(font=self.font, width=18, anchor=jra.CENTER, bd=5)
        self.menu = self.master.nametowidget(self.session_option.menuname)
        self.menu.config(font=self.font)
        self.session_option.grid(row=0, column=0)

        jra.Label(self.canvas_the_packer, bg="#0CEDCB").grid(row=2, column=0)
        self.pick_session = jra.Button(self.canvas_the_packer, width=15, font=self.font, text="Select This Session")
        self.pick_session.configure(bg="#EDE8BE", font=self.font, command=self.select_this_session, bd=5)
        self.pick_session.grid(row=3, column=0)
        jra.Label(self.canvas_the_packer, bg="#0CEDCB").grid(row=4, column=0, ipady=10)

        jra.Label(self.right_frame).grid(row=3, column=0)
        self.save_session = jra.Button(self.right_frame, text="Save Session", width=15, height=1)
        self.save_session.configure(bg="#DAEBEB", font=self.font, command=self.save_this_session)
        self.save_session.grid(row=4, column=0)
        jra.Label(self.right_frame).grid(row=5, column=0)
        self.deselected = jra.Button(self.right_frame, text="Deselected", width=15, height=1)
        self.deselected.configure(bg="#DAEBEB", font=self.font, command=self.deselected_all)
        self.deselected.grid(row=6, column=0)
        jra.Label(self.right_frame).grid(row=7, column=0)
        self.exit_button = jra.Button(self.right_frame, text="Cancel", width=15, height=1)
        self.exit_button.configure(bg="#DAEBEB", font=self.font, command=self.cancel_select)
        self.exit_button.grid(row=8, column=0)

        self.left_frame = jra.Frame(self.ROOT_FRAME)
        self.left_frame.grid(row=0, column=2)
        self.canvas = jra.Canvas(self.left_frame, width=int(w * 7.5 / 10), height=hCanvas, bg="#faf3e0")
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

        self.scroll_bar.pack(side=jra.RIGHT, fill=jra.Y)
        self.master.withdraw()
        self.button_size = 250
        list_users = ["phu", "BanHao", "Buttercup", "BeEm", "BeEm", "BeNhi", "ahTan", "beHung", "beHungZthung", "phu",
                      "phu3", "ahTan2", "HDVlog2"]
        self.add_all_user(list_all_user=list_users)

    def select_this_session(self):
        file_name = self.selected_session.get()
        if file_name.__eq__("Select Your Session"):
            return
        self.deselected_all()
        list_employee = []
        with open("Model/data/saved_sessions/"+file_name, "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                list_employee.append(i)
        self.picked_user = list_employee
        for temp_employee in self.picked_user:
            for temp_btn in self.list_buttons:
                if temp_btn.cget("text") == temp_employee:
                    print(temp_btn.cget("text"))
                    temp_btn.configure(bg="pink")
                    break

    def deselected_all(self):
        self.picked_user.clear()
        for temp_btn in self.list_buttons:
            temp_btn.configure(bg="#faf3e0")

    def let_save_session(self, session_name, backup_box_temp):
        session_name = str(session_name)

        str_names = ""
        for name in self.picked_user:
            if name != "None":
                str_names = str_names + name + " "
        filename = "Model/data/saved_sessions/" + session_name + ".txt"
        if not os.path.exists(filename):
            f = open(filename, "w")
            f.write(str_names)
            f.close()
            backup_box_temp.destroy()
        else:
            messagebox.showinfo("Error", "This name session is exists! Try again!")

    # Get input ID from user and do self.backup_plan()
    def save_this_session(self):
        backup_box = jra.Toplevel(self.master)
        backup_box.title("Session name")
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 445
        h = 160
        x, y = ws / 2 - w / 2, hs / 2 - h - 50
        backup_box.geometry('%dx%d+%d+%d' % (w, h, x, y))
        backup_id_entry = jra.Entry(backup_box, bg="#faf3e0", font=self.font, justify='center', width=23)
        backup_id_entry.grid(row=0, column=0, sticky="N", ipady=20)
        packet_label = jra.Label(backup_box, bg="#faf3e0")
        confirm_button = jra.Button(packet_label, text="Save", bg="#eabf9f", width=10, height=1, font=self.font,
                                    command=lambda: self.let_save_session(backup_id_entry.get(), backup_box))
        confirm_button.grid(row=0, column=0, sticky="SW")
        cancel_button = jra.Button(packet_label, text="Cancel", bg="#eabf9f", width=10, height=1, font=self.font,
                                   command=backup_box.destroy)
        cancel_button.grid(row=0, column=1, sticky="SE")
        packet_label.grid(row=1, column=0, sticky="S")
        backup_id_entry.focus_set()
        backup_id_entry.bind('<Return>', lambda event: self.let_save_session(backup_id_entry.get(), backup_box))
        self.saved_sesions = self.get_saved_sesion()

    def add_all_user(self, list_all_user):
        # get employee photo
        for user_id in list_all_user:
            user_id = str(user_id)
            num = 0
            found = False
            user_pic = Image.open("View/Stock/user-circle.png")
            while not found:
                if num > 20:
                    print("Wrong user picture!")
                    break
                try:
                    link_user = "Model/data/users_photos/" + user_id + "/" + str(num) + user_id + ".jpg"
                    num += 1
                    user_pic = Image.open(link_user)
                    found = True
                except FileNotFoundError:
                    found = False

            # get right size of user picture and resize to make it good looking and fit to the button
            img = ImageTk.PhotoImage(
                user_pic.resize(self.get_right_size(user_pic.width, user_pic.height), Image.ANTIALIAS))
            # add to self.list_images -> make it visible (I have tried make it simpler but it doesn't work)
            self.list_images.append(img)
            # do some math to grid in this window
            index = self.list_images.__len__() - 1

            button = jra.Button(self.secondFrame, image=self.list_images[index], text=user_id)
            button.configure(width=300, height=300, bg="#faf3e0")
            button.configure(command=lambda btn=button: self.pick_employee(btn))

            label = jra.Label(self.secondFrame, text=user_id, bg="#faf3e0", font=self.font)
            if self.column == 4:
                self.column = 0
                self.row += 2
            self.column += 1
            button.grid(row=self.row, column=self.column)
            label.grid(row=self.row + 1, column=self.column)
            # add to list_buttons -> take control this button
            self.list_buttons.append(button)
            self.list_labels.append(label)

    def pick_employee(self, btn):
        id_user = btn.cget("text")
        if id_user in self.picked_user:
            self.picked_user.pop(self.picked_user.index(id_user))
            btn.configure(bg="#faf3e0")
        elif id_user not in self.picked_user:
            self.picked_user.append(id_user)
            btn.configure(bg="pink")
        else:
            print("I don't know man! what the fuk?")
        print(self.picked_user)

    # def update_detected_text(self, num_of_list, num_of_left):
    #     # num_of_left += 1
    #     self.num_detected.configure(text=num_of_list - num_of_left)
    #     self.employee_left.configure(text=num_of_left)

    def cancel_select(self):
        # # stop detecting in Detector
        # self.menuUI.stop_detect()
        # hide this window
        self.master.withdraw()
        # # reset for new session
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
        # show this window
        self.master.deiconify()
        # start counting down

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

    def get_saved_sesion(self):
        saved_sesion = []
        for root, dirs, files in os.walk("Model/data/saved_sessions/"):
            saved_sesion = files
        return saved_sesion
