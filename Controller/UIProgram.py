from View.DetectedUser import DetectedUser
from View.Detector import Detector
from Model.train_all_classifiers import train_all_classifers
from Model.create_one_new_classifier import train_one_classifer
from Model.create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont, ttk
from tkinter import messagebox, PhotoImage

# from PIL import ImageTk, Image
# from gender_prediction import emotion,age And gender

names = []


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("Model/nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.append(i)
        self.title("Simple Face Attendance Recorder System")
        self.resizable(False, False)
        self.geometry("510x350")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None

        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            str_names = ""
            for name in names:
                if name != "None":
                    str_names = str_names + name + " "

            f = open("Model/nameslist.txt", "w")
            f.write(str_names)
            self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.timer_minute = 1
        new_window = tk.Toplevel(self)
        self.DetectedWindow = DetectedUser(new_window, self)
        self.controller = controller
        self.dec = None
        # load = Image.open("homepagepic.png")
        # load = load.resize((250, 250), Image.ANTIALIAS)
        render = PhotoImage(file='View/Stock/homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode="determinate")
        label = tk.Label(self, text="     Face Attendance     \n    Recorder System    ",
                         font=tkfont.Font(family='Helvetica', size=16, weight="bold"), fg="#263942")
        label.grid(row=0, sticky="ew")

        button1 = tk.Button(self, text="   Add a user  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))
        # button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",
        #                     command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="   Retrain dataset  ", fg="#ffffff", bg="#263942", command=self.train_data)
        button4 = tk.Button(self, text="   Recognition  ", fg="#ffffff", bg="#263942", command=self.openwebcam)
        button5 = tk.Button(self, text="    Quit    ", fg="#263942", bg="#ffffff", command=self.on_closing)

        button1.grid(row=1, column=0, ipady=3, ipadx=2)
        # button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=2, column=0, ipady=3, ipadx=2)
        button4.grid(row=3, column=0, ipady=3, ipadx=2)
        button5.grid(row=4, column=0, ipady=3, ipadx=2)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            str_names = ""
            for i in names:
                if i != "None":
                    str_names = str_names + i + " "

            f = open("Model/nameslist.txt", "w")
            f.write(str_names)
            self.controller.destroy()

    def train_data(self):
        global names
        messagebox.showinfo("INSTRUCTIONS", "Wait a few minute.... we are training!")
        self.controller.list_users = train_all_classifers()
        names = self.controller.list_users

    def openwebcam(self):
        global names
        if names is not None:
            print("Detecting....")
            self.progress_bar.grid(row=4, column=1, sticky="nsew")
            self.dec = Detector(names, self)
            self.dec.start()
        else:
            messagebox.showinfo("INSTRUCTIONS", "List users is empty. Let add someone first!")

    def detected_user_from_detector(self,id_to_check):
        # return index of the user
        checked_id = self.dec.find_index_of_users(id_to_check)
        # if this id in Detector
        if checked_id is not None:
            return checked_id
        # if this id not in Detector check again in Loaded Employee list
        else:
            if checked_id not in names:
                # if this id not in Loaded Employee so -> this ID doesn't exist in system
                return None
            else:
                # if this id Loaded Employee so -> this ID already check in by face ID before.
                # So i choose to add this Employee in Detector again and recheck this Employee ONE MORE TIME
                self.dec.add_backup_user(id_to_check)
                checked_id_second = self.dec.find_index_of_users(id_to_check)
                messagebox.showinfo("This Employee already check in before!")
                return checked_id_second


    def open_detect_UI(self):
        self.progress_bar.grid_forget()
        self.controller.withdraw()

        self.DetectedWindow.show(self.timer_minute)

    def update_detected_text(self, num_of_list, num_of_left):
        self.DetectedWindow.update_detected_text(num_of_list=num_of_list, num_of_left=num_of_left)

    def add_detected_user(self, user_id):
        self.DetectedWindow.add_detected_user(user_id)

    def update_frame(self, frame):
        self.DetectedWindow.update_image(frame)

    def stop_detect(self):
        self.dec.stop_detect()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10,
                                                                                           padx=5)
        self.student_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.student_name.grid(row=0, column=1, pady=10, padx=10)
        self.button_cancel = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942",
                                       command=lambda: controller.show_frame("StartPage"))
        self.button_next = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.button_cancel.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.button_next.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)

    def start_training(self):
        global names
        if self.student_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.student_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.student_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.student_name.get()
        names.append(name)
        self.controller.active_name = name
        # self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10,
                                                                                        pady=10)
        self.button_cancel = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"),
                                       bg="#ffffff", fg="#263942")
        self.menu_var = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menu_var, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.button_next = tk.Button(self, text="Next", command=self.next_foo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.button_cancel.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.button_next.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def next_foo(self):
        if self.menu_var.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menu_var.get()
        self.controller.show_frame("StartPage")


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.num_of_images = 0
        self.num_label = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.num_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capture_button = tk.Button(self, text="Capture Data Set", fg="#ffffff",
                                        bg="#263942", command=self.capturing)
        self.back_to_menu = tk.Button(self, text="  Back To Menu  ", fg="#ffffff", bg="#263942", command=self.show_menu)
        self.train_button = tk.Button(self, text="Train the model of this user", fg="#ffffff", bg="#263942",
                                      command=self.train_model)
        self.capture_button.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.train_button.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capturing(self):
        messagebox.showinfo("INSTRUCTIONS", "Wait to capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.num_label.config(text=str("Number of images captured = " + str(x) + ". Let retrain your dataset now!"))
        self.back_to_menu.grid(row=2, column=0, ipadx=5, ipady=4, padx=10, pady=20)

    def show_menu(self):
        self.controller.show_frame("StartPage")

    def train_model(self):
        if self.controller.num_of_images <= 0:
            messagebox.showinfo("INSTRUCTIONS", "Let take some photos!")
        elif 200 > self.controller.num_of_images > 0:
            if messagebox.askokcancel("WARNING", "Data is not enough that will effect to your result. Do you want to "
                                                 "continue?"):
                messagebox.showinfo("INSTRUCTIONS", "Wait a few minute.... we are training!")
                train_one_classifer(self.controller.active_name)
                messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
                self.controller.show_frame("StartPage")
        else:
            messagebox.showinfo("INSTRUCTIONS", "Wait a few minute.... we are training!")
            train_one_classifer(self.controller.active_name)
            messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
            self.controller.show_frame("StartPage")
