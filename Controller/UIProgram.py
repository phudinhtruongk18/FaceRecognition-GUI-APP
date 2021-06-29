import os

from Controller.DetectedUser import DetectedUser
from Model.ClassForSoftware import Employee
from Model.make_and_send.excel_maker import create_excel_by_time
from View.Detector import Detector
from Model.train_all_classifiers import train_all_classifers
from Model.create_one_new_classifier import train_one_classifer
from Model.create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont, ttk
from tkinter import messagebox, PhotoImage
from Controller.SelectSession import SelectSession
from Model.data_manager import DataManager
from tkcalendar import DateEntry


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Face Attendance Recorder System")
        self.resizable(False, False)
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x, y = ws / 2 - 610 / 2, hs / 2 - 370
        self.geometry('%dx%d+%d+%d' % (610, 370, x, y))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_employee = None

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
            self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.timer_minute = 0

        self.controller = controller
        self.dec = None
        self.current_session = None
        self.DetectedWindow = None

        render = PhotoImage(file='View/Stock/homepagepic.png')
        img = tk.Label(self, image=render)
        img.image = render
        img.grid(row=0, column=1, rowspan=5, ipadx=50, sticky="nsew")
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=100, mode="determinate")
        about = tk.Button(self, width=20, text="    About    ", fg="#ffffff", bg="#263942", command=self.show_about)
        tk.Label(self).grid(row=6, column=1, ipady=2, ipadx=2)
        about.grid(row=7, column=1, ipady=6, ipadx=6)
        label = tk.Label(self, text="     Face Attendance     \n    Recorder System    ",
                         font=tkfont.Font(family='Helvetica', size=16, weight="bold"), fg="#263942")
        label.grid(row=0, sticky="ew")

        label1 = tk.Label(self)
        label1.grid(row=1, column=0, ipady=3, ipadx=2)

        button1 = tk.Button(label1, text="   Add a user  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageOne"))

        button2 = tk.Button(label1, text="   Change Infor  ", fg="#ffffff", bg="#263942",
                            command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="  Retrain dataset ", fg="#ffffff", bg="#263942", command=self.train_data)
        button4 = tk.Button(self, text="   Select Session  ", fg="#ffffff", bg="#263942", command=self.select_session)
        button5 = tk.Button(self, text="   Start Session  ", fg="#ffffff", bg="#263942", command=self.openwebcam)
        button6 = tk.Button(self, text="   Export Result  ", fg="#ffffff", bg="#263942", command=self.open_export_box)
        button7 = tk.Button(self, text="    Quit    ", fg="#263942", bg="#ffffff", command=self.on_closing)

        button1.grid(row=1, column=0, ipady=3, ipadx=2)
        button2.grid(row=1, column=1, ipady=3, ipadx=2)

        button3.grid(row=2, column=0, ipady=4, ipadx=2)
        button4.grid(row=3, column=0, ipady=4, ipadx=2)
        button5.grid(row=4, column=0, ipady=4, ipadx=2)
        button6.grid(row=5, column=0, ipady=4, ipadx=2)
        tk.Label(self).grid(row=6, column=0, ipady=2, ipadx=2)
        button7.grid(row=7, column=0, ipady=4, ipadx=5)

    def export_data(self, cal1, cal2, export_box):
        if cal1 >= cal2:
            messagebox.showinfo("Wrong time", "Choose time again!")
            return
        filename = create_excel_by_time(cal1, cal2)
        export_box.destroy()
        self.controller.deiconify()
        if messagebox.askokcancel("Export complete!", "Do you want to open " + filename + "!"):
            self.open_fordel()

    def open_fordel(self):
        os.startfile(f'{os.path.realpath("View/Summary")}')

    def open_export_box(self):
        self.controller.withdraw()
        export_box = tk.Toplevel(self.master)
        export_box.title("Export Data Box")
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 305
        h = 200
        x, y = ws / 2 - w / 2, hs / 2 - h - 80
        export_box.geometry('%dx%d+%d+%d' % (w, h, x, y))
        label = tk.Label(export_box, width=30, text="From")
        label2 = tk.Label(export_box, width=30, text="To")
        cal1 = DateEntry(export_box, width=10, bg="darkblue", fg="white", year=2021, month=6, day=12,
                         date_pattern='y-mm-dd', font=('Helvetica', 18, "bold"))
        cal2 = DateEntry(export_box, width=10, bg="darkblue", fg="white", year=2021, month=6, day=14,
                         date_pattern='y-mm-dd', font=('Helvetica', 18, "bold"))
        btn = tk.Button(export_box, width=10, text="Export", fg="#ffffff", bg="#263942", font=('Helvetica', 18, "bold"),
                        command=lambda: self.export_data(cal1.get(), cal2.get(), export_box))
        export_box.protocol("WM_DELETE_WINDOW", lambda: self.close_export(export_box))
        label.pack()
        cal1.pack()
        label2.pack()
        cal2.pack()
        tk.Label(export_box).pack()
        btn.pack()

    def close_export(self, export_box):
        export_box.destroy()
        self.controller.deiconify()

    def show_about(self):
        about_box = tk.Toplevel(self.master)
        about_box.title("About")
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 605
        h = 300
        x, y = ws / 2 - w / 2, hs / 2 - h
        about_box.geometry('%dx%d+%d+%d' % (w, h, x, y))
        label = tk.Label(about_box, width=60, text="""
Original FaceRecognition-GUI-APP by JoeVenner
Thank JoeVenner for allowing me to develop this awesome project

SIMPLE FACE ATTENDANCE RECORDER SYSTEM
Instructor: MSIT Vũ Đình Long
Main develop and design: Phu Dinh Truong - phudinhtruongk18@gmail.com
Special thank to for great support: Pham Van Luong with Sang Nguyen
Web Front-End Designer: Pham Thanh Long
            """, font=('Helvetica', 12, "bold"))
        btn = tk.Button(about_box, width=10, text="Close", fg="#ffffff", bg="#263942", font=('Helvetica', 13, "bold"),
                        command=about_box.destroy)
        label.pack()
        tk.Label(about_box).pack()
        btn.pack()

    def get_select_list(self, selected_session):
        self.current_session = selected_session

    def select_session(self):
        new_window2 = tk.Toplevel(self)
        SelectWindow = SelectSession(new_window2, self)
        with DataManager('Model/data/database/database.db') as db:
            ALL_ID = db.get_load_infor()
        self.controller.withdraw()
        SelectWindow.show(ALL_ID)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure?"):
            self.controller.destroy()

    def train_data(self):
        messagebox.showinfo("INSTRUCTIONS", "Wait a few minute.... we are training!")
        self.controller.list_users = train_all_classifers()

    def openwebcam(self):

        if not self.current_session:
            messagebox.showerror("Error", "Select session first!")
            return
        with DataManager('Model/data/database/database.db') as db:
            # get employee in selected session
            ALL_ID = db.get_all_employee_by_session_ID(self.current_session)
            # get timer for UI_detected_user
            self.timer_minute = db.get_duration_by_session_ID(self.current_session)
            # create new RECORDER for session and get ID_RECORDER back
            ID_RECORDER = db.insert_and_get_id_recorder(self.current_session)
        if ID_RECORDER is not None:
            print("Success create new RECORDER ", ID_RECORDER)
        else:
            messagebox.showinfo("Database error", "Something wrong when create new ID_RECORDER in UIProgram")
            return
        new_window = tk.Toplevel(self)
        self.DetectedWindow = DetectedUser(new_window, self)

        if ALL_ID:
            print("Detecting....")
            self.progress_bar['value'] = 0
            self.progress_bar.grid(row=5, column=1, sticky="nsew")

            self.dec = Detector(ID_RECORDER, ALL_ID, self)
            self.dec.start()
        else:
            messagebox.showinfo("INSTRUCTIONS", "List users is empty. Let add someone first!")

    def backup_detected_user_with_id_to_detector(self, id_to_backup, detected_times):
        # call dec to work with sql
        if detected_times > 0:
            self.dec.backup_detected_user_with_id_but_detected_before(id_to_backup)
        else:
            self.dec.backup_detected_user_with_id(id_to_backup)

    def find_state_of_users_by_id(self, id_to_check):
        times = self.dec.find_state_of_users(id_to_check)
        return times

    def detected_user_from_detector(self, id_to_check):
        # this method
        # return isRecorded = false and detected_times if employee ID non attendance yet
        # return isRecorded = true and detected_times if employee ID attendance already
        # return None and None if ID doesn't exist in system

        # return detected_time of the employee
        detected_times = self.find_state_of_users_by_id(id_to_check)
        if detected_times > 0:
            # if this id Loaded Employee so -> this ID already check in by face ID before.
            return True, detected_times
        # if this id not in Detector check again in Loaded Employee list
        else:
            with DataManager('Model/data/database/database.db') as db:
                all_id = db.get_all_employee_id_by_session_ID(self.current_session)
            if id_to_check not in all_id:
                # if this id not in Loaded Employee so -> this ID doesn't exist in system
                return None, None
            else:
                # if this id Loaded Employee in list but doesn't recognize
                return False, detected_times

    def open_detect_UI(self):
        self.progress_bar.grid_forget()
        self.controller.withdraw()
        with DataManager('Model/data/database/database.db') as db:
            list_employee = db.get_all_employee_by_session_ID(self.current_session)
        self.DetectedWindow.show(self.timer_minute, list_employee)

    def update_detected_text(self, num_of_list, num_of_left):
        self.DetectedWindow.update_detected_text(num_of_list=num_of_list, num_of_left=num_of_left)

    def add_detected_user(self, user_id, detected_time):
        self.DetectedWindow.add_detected_user(user_id, detected_time)

    def add_detected_user_backup(self, user_id, detected_time):
        self.DetectedWindow.add_detected_user_backup(user_id, detected_time)

    def update_frame(self, frame):
        self.DetectedWindow.update_image(frame)

    def stop_detect(self):
        self.dec.stop_detect()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="ID", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.employee_ID = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_ID.grid(row=0, column=1, pady=10, padx=10)
        tk.Label(self, text="NAME", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0, pady=10, padx=5)
        self.employee_NAME = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_NAME.grid(row=1, column=1, pady=10, padx=10)
        tk.Label(self, text="SEX", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0, pady=10, padx=5)
        self.employee_SEX = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_SEX.grid(row=2, column=1, pady=10, padx=10)
        tk.Label(self, text="AGE", fg="#263942", font='Helvetica 12 bold').grid(row=3, column=0, pady=10, padx=5)
        self.employee_AGE = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_AGE.grid(row=3, column=1, pady=10, padx=10)
        tk.Label(self, text="UNIT", fg="#263942", font='Helvetica 12 bold').grid(row=4, column=0, pady=10, padx=5)
        self.employee_UNIT = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_UNIT.grid(row=4, column=1, pady=10, padx=10)

        self.button_cancel = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942",
                                       command=lambda: controller.show_frame("StartPage"))
        self.button_next = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.button_cancel.grid(row=6, column=0, pady=10, ipadx=5, ipady=4)
        self.button_next.grid(row=6, column=1, pady=10, ipadx=5, ipady=4)

    def start_training(self):
        with DataManager('Model/data/database/database.db') as db:
            ALL_ID = db.get_all_user_ID()
        if self.employee_ID.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.employee_ID.get() in ALL_ID:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.employee_ID.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        try:
            employ_ID = self.employee_ID.get()
            employ_NAME = self.employee_NAME.get()
            employ_AGE = int(self.employee_AGE.get())
            if employ_AGE < 1:
                messagebox.showinfo("Wrong Age", "You are too young for working! Grow up and try again!")
                return
            employ_SEX = self.employee_SEX.get()
            employ_UNIT = self.employee_UNIT.get()
        except TypeError as type_error:
            messagebox.showinfo("Wrong format", str(type_error))
            return
        except Exception as e:
            messagebox.showinfo("Exception error", str(e))
            return
        if "" in [employ_NAME, employ_AGE, employ_SEX, employ_UNIT]:
            messagebox.showinfo("Not allow Null", "Type all there information!")
            return

        temp_employee = Employee(employ_ID, employ_NAME, employ_SEX, employ_AGE, employ_UNIT)

        self.controller.active_employee = temp_employee
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.note_label = tk.Label(self, text="Update employee information", fg="#263942", font='Helvetica 12 bold')
        self.note_label.grid(row=0, column=0)
        self.menu_var = tk.StringVar(self)

        self.employee_detail = tk.Label(self)

        self.label_ID = tk.Label(self.employee_detail)
        self.label_ID.grid(row=0, column=0)

        tk.Label(self.label_ID, text="ID", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0)
        self.employee_ID = tk.Entry(self.label_ID, borderwidth=2, bg="lightgrey", font='Helvetica 11')
        self.employee_ID.grid(row=1, column=0)

        self.employee_detail2 = tk.Label(self.employee_detail)

        tk.Label(self.employee_detail2, text="NAME", fg="#263942", font='Helvetica 12 bold').grid(row=1, column=0,
                                                                                                  pady=10, padx=5)
        self.employee_NAME = tk.Entry(self.employee_detail2, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_NAME.grid(row=1, column=1, pady=10, padx=10)
        tk.Label(self.employee_detail2, text="SEX", fg="#263942", font='Helvetica 12 bold').grid(row=2, column=0,
                                                                                                 pady=10, padx=5)
        self.employee_SEX = tk.Entry(self.employee_detail2, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_SEX.grid(row=2, column=1, pady=10, padx=10)
        tk.Label(self.employee_detail2, text="AGE", fg="#263942", font='Helvetica 12 bold').grid(row=3, column=0,
                                                                                                 pady=10, padx=5)
        self.employee_AGE = tk.Entry(self.employee_detail2, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_AGE.grid(row=3, column=1, pady=10, padx=10)
        tk.Label(self.employee_detail2, text="UNIT", fg="#263942", font='Helvetica 12 bold').grid(row=4, column=0,
                                                                                                  pady=10, padx=5)
        self.employee_UNIT = tk.Entry(self.employee_detail2, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.employee_UNIT.grid(row=4, column=1, pady=10, padx=10)

        self.label_button = tk.Label(self)
        self.button_cancel = tk.Button(self.label_button, text="Cancel",
                                       command=lambda: controller.show_frame("StartPage"),
                                       bg="#ffffff", fg="#263942")
        self.button_next = tk.Button(self.label_button, text="Next", command=self.get_to_update, fg="#ffffff",
                                     bg="#263942")
        self.button_update = tk.Button(self.label_button, text="Update", command=self.update_to_database, fg="#ffffff",
                                       bg="#263942")
        self.button_delete = tk.Button(self.label_button, text="Delete", command=self.delete_to_database, fg="#ffffff",
                                       bg="#263942")
        self.button_cancel.grid(row=0, ipadx=10, ipady=4, column=0, pady=10)
        tk.Label(self.label_button).grid(row=0, column=1, pady=10, padx=10)
        tk.Label(self.label_button).grid(row=0, column=3, pady=10, padx=10)
        self.button_next.grid(row=0, ipadx=10, ipady=4, column=2, pady=10)
        self.employee_detail.grid(row=1, column=0, ipadx=8, padx=10, pady=10)
        self.label_button.grid(row=2, column=0, ipadx=8, padx=10, pady=10)

    def get_to_update(self):
        ID_EMPLOYEE = self.employee_ID.get()
        with DataManager('Model/data/database/database.db') as db:
            change_employee = db.get_employee_infor_by_id(ID_EMPLOYEE)
            if change_employee is None:
                messagebox.showinfo("Empty", "This ID doesn't exist!")
                return None
        self.employee_ID.configure(state='disabled')
        employee_to_change = Employee(*change_employee)
        self.hide_things(employee_to_change)

    def delete_to_database(self):
        self.employee_ID.configure(state='disabled')
        ID_EMPLOYEE = self.employee_ID.get()
        if messagebox.askokcancel("Are you sure?", "Delete the employee with ID :" + ID_EMPLOYEE):
            with DataManager('Model/data/database/database.db') as db:
                if not db.delete_employee_by_id(ID_EMPLOYEE=ID_EMPLOYEE):
                    messagebox.showinfo("Something went wrong!", "Try again")
            self.show_things()

    def update_to_database(self):
        with DataManager('Model/data/database/database.db') as db:
            employee_ID = self.employee_ID.get()
            employee_NAME = self.employee_NAME.get()
            employee_AGE = self.employee_AGE.get()
            employee_SEX = self.employee_SEX.get()
            employee_UNIT = self.employee_UNIT.get()

            change_employee = db.update_employee_infor_by_id(ID_EMPLOYEE=employee_ID, NAME=employee_NAME,
                                                             AGE=employee_AGE,
                                                             SEX=employee_SEX, UNIT=employee_UNIT)
            if change_employee is None:
                messagebox.showinfo("Empty", "This ID doesn't exist!")
                return None
            elif not change_employee:
                return
        self.show_things()
        messagebox.showinfo("Success", "Update success!")

    def show_things(self):
        self.employee_ID.configure(state='normal')
        self.employee_ID.delete(0, "end")
        self.button_delete.grid_forget()
        self.button_update.grid_forget()
        self.employee_detail2.grid_forget()
        self.note_label.configure(text="Update employee information")
        self.label_ID.grid(row=0, column=0)
        self.button_next.grid(row=0, ipadx=10, ipady=4, column=2, pady=10)
        self.button_cancel.grid(row=6, column=0, pady=10, ipadx=5, ipady=4)

    def hide_things(self, employee):
        self.label_ID.grid_forget()
        self.employee_detail2.grid(row=0, column=1)
        self.note_label.configure(text="Update " + employee.ID + " detail")
        self.employee_NAME.delete(0, "end")
        self.employee_NAME.insert(0, employee.name)
        self.employee_AGE.delete(0, "end")
        self.employee_AGE.insert(0, employee.age)
        self.employee_SEX.delete(0, "end")
        self.employee_SEX.insert(0, employee.sex)
        self.employee_UNIT.delete(0, "end")
        self.employee_UNIT.insert(0, employee.unit)
        self.button_next.grid_forget()
        self.button_update.grid(row=0, ipadx=10, ipady=4, column=2, pady=10)
        self.button_delete.grid(row=0, ipadx=10, ipady=4, column=4, pady=10)


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
        x = start_capture(self.controller.active_employee.ID)
        self.controller.num_of_images = x
        # save this employee to database
        with DataManager('Model/data/database/database.db') as db:
            if db.insert_employee(self.controller.active_employee):
                print("Success")
            else:
                print("Fail")
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
                train_one_classifer(self.controller.active_employee.ID)
                messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
                self.controller.show_frame("StartPage")
        else:
            messagebox.showinfo("INSTRUCTIONS", "Wait a few minute.... we are training!")
            train_one_classifer(self.controller.active_employee.ID)
            messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
            self.controller.show_frame("StartPage")
