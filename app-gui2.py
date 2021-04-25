from Detector import detector
from create_classifier import train_classifer
from create_one_new_classifier import train_one_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox, PhotoImage

# from PIL import ImageTk, Image
# from gender_prediction import emotion,age And gender
names = []


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.append(i)
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("500x350")
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

            f = open("nameslist.txt", "w")
            f.write(str_names)
            self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # load = Image.open("homepagepic.png")
        # load = load.resize((250, 250), Image.ANTIALIAS)
        render = PhotoImage(file='homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=4, sticky="nsew")
        label = tk.Label(self, text="        Home Page        ", font=self.controller.title_font, fg="#263942")
        label.grid(row=0, sticky="ew")

        button1 = tk.Button(self, text="   Add a user  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="   Retrain dataset  ", fg="#ffffff", bg="#263942", command=self.train_data)
        button4 = tk.Button(self, text="   Recognition  ", fg="#ffffff", bg="#263942", command=self.openwebcam)
        button5 = tk.Button(self, text="    Quit    ", fg="#263942", bg="#ffffff", command=self.on_closing)

        button1.grid(row=1, column=0, ipady=3, ipadx=2)
        button2.grid(row=2, column=0, ipady=3, ipadx=2)
        button3.grid(row=3, column=0, ipady=3, ipadx=2)
        button4.grid(row=4, column=0, ipady=3, ipadx=2)
        button5.grid(row=5, column=0, ipady=3, ipadx=2)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            str_names = ""
            for i in names:
                if i != "None":
                    str_names = str_names + i + " "

            f = open("nameslist.txt", "w")
            f.write(str_names)
            self.controller.destroy()

    def train_data(self):
        global names
        messagebox.showinfo("INSTRUCTIONS", "Wait a few minute.... we are training!")
        self.controller.list_users = train_classifer()
        names = self.controller.list_users

    def openwebcam(self):
        global names
        if names is not None:
            print("Detecting....")
            dec = detector(names)
            dec.main_app()
        else:
            messagebox.showinfo("INSTRUCTIONS", "List users is empty. Let add someone first!")


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10,
                                                                                           padx=5)
        self.student_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.student_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942",
                                    command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)

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
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"),
                                    bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("StartPage")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.num_of_images = 0
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train the model of this user", fg="#ffffff", bg="#263942", command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        messagebox.showinfo("INSTRUCTIONS", "Wait to capture 200 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = " + str(x) + ". Let retrain your dataset now!"))

    def trainmodel(self):
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


# class PageFour(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#
#         label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
#         label.grid(row=0, column=0, sticky="ew")
#         button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
#         # button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
#         # button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")
#         button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"),
#                             bg="#ffffff", fg="#263942")
#         button1.grid(row=1, column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#         # button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#         # button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#         button4.grid(row=1, column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
#
#     def openwebcam(self):
#         print(self.controller.list_users)
#         dec = detector(self.controller.list_users)
#         dec.main_app()
# def gender_age_pred(self):
#  ageAndgender()
# def emot(self):
#   emotion()


app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()
