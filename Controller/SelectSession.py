from tkinter import ttk, messagebox
import tkinter as jra
from PIL import ImageTk, Image

from Model.ClassForSoftware import ListEmployee, Session
from Model.data_manager import DataManager


class SelectSession:
    def __init__(self, master_temp=None, menuUI=None):
        self.picked_user_IDs = []
        self.menuUI = menuUI
        self.master = master_temp

        self.master.title("Select Session")
        w, h = int(self.master.winfo_screenwidth() * 5 / 6) + 50, int(self.master.winfo_screenheight() * 5 / 6)
        hCanvas = h - 27
        x = int(self.master.winfo_screenwidth() / 2 - w / 2)
        y = int(self.master.winfo_screenheight() / 2 - h * 1.1 / 2)

        self.master.geometry("{0}x{1}+{2}+{3}".format(w, hCanvas, x, y))

        self.font = ('Helvetica', 20, "bold")

        self.ROOT_FRAME = jra.Frame(self.master, height=hCanvas)
        self.ROOT_FRAME.grid(row=0, column=0)
        self.right_frame = ttk.Frame(self.ROOT_FRAME)
        self.right_frame.grid(row=0, column=1, sticky=jra.N)

        self.canvas_the_packer = jra.Canvas(self.right_frame, bg="#0CEDCB")
        self.canvas_the_packer.grid(row=1, column=0)

        self.infor_label = jra.Label(self.canvas_the_packer, bg="#0CEDCB", text="Your Saved Data",
                                     font=('Helvetica', 20, "bold"), width=22)
        self.infor_label.grid(row=0, column=0, ipady=10)

        self.canvas_option = jra.Canvas(self.canvas_the_packer, width=19)
        self.canvas_option.grid(row=1, column=0)

        self.string_selected_session = jra.StringVar(self.master, value="Select Your Session")

        self.session_option_menu = jra.OptionMenu(self.canvas_option, self.string_selected_session, None)
        self.session_option_menu.configure(font=self.font, width=18, anchor=jra.CENTER, bd=5)
        self.menu_option = self.master.nametowidget(self.session_option_menu.menuname)
        self.menu_option.config(font=self.font)
        self.session_option_menu.grid(row=0, column=0)
        # change the picked employee when change the session
        self.string_selected_session.trace("w", self.show_this_session)

        jra.Label(self.canvas_the_packer, bg="#0CEDCB").grid(row=2, column=0)
        self.pick_session_btn = jra.Button(self.canvas_the_packer, width=15, font=self.font, text="Select This!")
        self.pick_session_btn.configure(bg="#EDE8BE", font=self.font, command=self.select_this_session, bd=5)
        self.pick_session_btn.grid(row=3, column=0)
        jra.Label(self.canvas_the_packer, bg="#0CEDCB").grid(row=4, column=0, ipady=10)

        self.time_label = jra.Label(self.right_frame)
        self.time_label.grid(row=3, column=0)
        jra.Label(self.time_label).grid(row=0, column=0, ipady=1)
        self.guide_time_label = jra.Label(self.time_label, text="Duration: ",
                                          font=('Helvetica', 18, "bold"), width=8)
        self.guide_time_label.grid(row=1, column=0, ipady=10)
        self.time_entry = jra.Entry(self.time_label, font=self.font, bg="#C2F5F0", justify='center', width=4)
        self.time_entry.grid(row=1, column=1, ipady=5)
        self.guide_time_label2 = jra.Label(self.time_label, text="min",
                                           font=('Helvetica', 18, "bold"), width=4)
        self.guide_time_label2.grid(row=1, column=3, ipady=5)
        jra.Label(self.time_label).grid(row=2, column=0, ipady=1)

        self.save_session_btn = jra.Button(self.right_frame, text="Save", width=15, height=1)
        self.save_session_btn.configure(bg="#DAEBEB", font=self.font, command=self.save_this_session)
        self.save_session_btn.grid(row=4, column=0)
        jra.Label(self.right_frame).grid(row=5, column=0)
        self.deselected_btn = jra.Button(self.right_frame, text="Deselected", width=15, height=1)
        self.deselected_btn.configure(bg="#DAEBEB", font=self.font, command=self.deselected_all)
        self.deselected_btn.grid(row=6, column=0)
        jra.Label(self.right_frame).grid(row=7, column=0)
        self.delete_saved_one = jra.Button(self.right_frame, text="Delete", width=15, height=1)
        self.delete_saved_one.configure(bg="#DAEBEB", font=self.font, command=self.delete_current_one)
        self.delete_saved_one.grid(row=8, column=0)
        jra.Label(self.right_frame).grid(row=9, column=0)
        self.exit_button = jra.Button(self.right_frame, text="Cancel", width=15, height=1)
        self.exit_button.configure(bg="#DAEBEB", font=self.font, command=self.cancel_select)
        self.exit_button.grid(row=10, column=0)

        self.left_frame = jra.Frame(self.ROOT_FRAME)
        self.left_frame.grid(row=0, column=2)
        self.canvas = jra.Canvas(self.left_frame, width=int(w * 7.5 / 10), height=hCanvas, bg="#faf3e0")
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
        self.button_size = 230

        self.list_all_user = None
        self.session_list = []
        self.list_unit_label = []
        self.found_session = None

    def open_confirm_window(self):
        confirm_box = jra.Toplevel(self.master)
        confirm_box.title("Confirm Window")
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 600
        h = 500
        x, y = ws / 2 - w / 2 - 50, hs / 2 - h / 2
        confirm_box.geometry('%dx%d+%d+%d' % (w, h, x, y))
        confirm_box.configure(bg="#faf3e0")
        employee_in_session = self.get_all_name_employee_by_id_session(self.found_session.ID)
        string_employee = "\n"
        column = 1
        for index, temp_employee in enumerate(employee_in_session):
            string_employee += temp_employee
            if column == 4:
                string_employee += "\n"
                column = 0
            else:
                string_employee += " - "
            column += 1
        detail_about_session = f'Session ID :{self.found_session.ID}\nSession Name :' \
                               f'{self.found_session.name}\nSession Duration :{self.found_session.duration}' \
                               f'\nEmployee in your session :'
        infor_session_label = jra.Label(confirm_box, fg="#263942", bg="#faf3e0", justify='left',
                                        text=detail_about_session, font=self.font, width=35, height=3)
        infor_session_label.grid(row=0, column=0, ipady=20)
        infor_employee_label = jra.Label(confirm_box, fg="#263942", bg="#faf3e0", text=string_employee,
                                         font=('Helvetica', 15, "bold"))
        infor_employee_label.grid(row=1, column=0)
        packet_label = jra.Label(confirm_box, bg="#faf3e0")
        confirm_button = jra.Button(packet_label, text="Confirm", bg="#eabf9f", width=10, height=1, font=self.font,
                                    command=lambda: self.confirm_and_close(confirm_box))
        confirm_button.grid(row=0, column=0)
        cancel_button = jra.Button(packet_label, text="Cancel", bg="#eabf9f", width=10, height=1, font=self.font,
                                   command=confirm_box.destroy)
        cancel_button.grid(row=0, column=1)
        packet_label.grid(row=2, column=0)
        # backup_id_entry.bind('<Return>', lambda event: self.backup_plan(backup_id_entry.get(), backup_box))

    def confirm_and_close(self, confirm_box):
        ID_session = str(self.found_session.ID)
        self.menuUI.get_select_list(ID_session)
        confirm_box.destroy()
        self.cancel_select()

    def delete_current_one(self):
        if messagebox.askokcancel("Delete", "Are you sure?"):
            # work with sql later on
            print("xoa ne chac chua")
            session_ID = self.found_session.ID
            with DataManager('Model/data/database/database.db') as db:
                if db.delete_session_by_id(session_ID):
                    print("Delete session success")
                else:
                    print("Wrong in database db.delete_session_by_id")
                    return
            self.deselected_all()
            self.string_selected_session.set("Select Your Session")
            self.reset_saved_sesions()

    def select_this_session(self):
        if self.found_session is None:
            messagebox.showinfo("Empty selection", "Please choose again!")
            return
        self.open_confirm_window()

    def get_session_session_list_by_id(self, find_id):
        for temp_session in self.session_list:
            if temp_session.ID == find_id:
                return temp_session
        return None

    def get_all_id_employee_by_id_session(self, found_session_ID):
        with DataManager('Model/data/database/database.db') as db:
            list_employee_id = db.get_all_employee_id_by_session_ID(found_session_ID)
        return list_employee_id

    def get_all_name_employee_by_id_session(self, found_session_ID):
        with DataManager('Model/data/database/database.db') as db:
            list_employee_name = db.get_all_employee_name_by_session_ID(found_session_ID)
        return list_employee_name

    def show_this_session(self, *args):
        # get id of session in menu option
        self.found_session = None
        self.picked_user_IDs.clear()

        id_of_session = self.string_selected_session.get()
        if id_of_session.__eq__("Select Your Session"):
            print("Something wrong with data")
            return None
        # get session information by id in list_session
        self.found_session = self.get_session_session_list_by_id(id_of_session)

        if not self.found_session:
            print("Something wrong in tracing of SelectSession!")
        self.string_selected_session.set(self.found_session.name)
        self.deselected_all()

        self.picked_user_IDs = self.get_all_id_employee_by_id_session(self.found_session.ID)
        for temp_employee in self.picked_user_IDs:
            for temp_btn in self.list_buttons:
                if temp_btn.cget("text") == temp_employee:
                    temp_btn.configure(bg="pink")
                    break
        self.time_entry.delete(0, "end")
        self.time_entry.insert(0, self.found_session.duration)

    def deselected_all(self):
        self.picked_user_IDs.clear()
        for temp_btn in self.list_buttons:
            temp_btn.configure(bg="#faf3e0")

    def let_save_session(self, duration, session_id, session_name, add_box_temp):
        # check empty
        if session_id is "":
            messagebox.showinfo("Empty", "Fill ID entry")
            return
        if session_name is "":
            messagebox.showinfo("Empty", "Fill name entry")
            return
        # covert string
        session_id = str(session_id)
        session_name = str(session_name)

        # check exist
        for temp_session in self.session_list:
            if temp_session.ID == session_id:
                messagebox.showinfo("Exist", "This session ID is exist! Try again!")
                return

        # become Session obj
        session_to_insert = Session(session_id, session_name, duration)

        # push to database
        with DataManager('Model/data/database/database.db') as db:
            if db.insert_session(session_to_insert):
                print("Done", "Add session complete")
            else:
                messagebox.showinfo("Wrong in database", "Can't add this employee! Try Again")
                return
            if db.insert_list_id_employee_to_saved_id_session(list_id_employee=self.picked_user_IDs,
                                                              id_session=session_to_insert.ID):
                print("Successful! ", session_id, self.picked_user_IDs)
            else:
                print("Fail!")

        self.string_selected_session.set("Select Your Session")
        self.reset_saved_sesions()
        add_box_temp.destroy()

    def save_this_session(self):
        try:
            duration = int(self.time_entry.get())
            if duration < 1:
                messagebox.showinfo("Error", "Wrong duration!")
            self.open_save_session_box(duration)
        except Exception as e:
            print(e)
            messagebox.showinfo("Error", "Wrong duration format!")

    def open_save_session_box(self, duration):
        backup_box = jra.Toplevel(self.master)
        backup_box.title("Save session")
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        w = 463
        h = 139
        x, y = ws / 2 - w / 2, hs / 2 - h - 50
        backup_box.geometry('%dx%d+%d+%d' % (w, h, x, y))

        label_and_entry = jra.Label(backup_box)

        id_ss_label = jra.Label(label_and_entry, text="ID", font=self.font, justify='center', width=5)
        id_ss_label.grid(row=0, column=0)
        name_ss_label = jra.Label(label_and_entry, text="Name", font=self.font, justify='center', width=5)
        name_ss_label.grid(row=1, column=0)
        id_ss_entry = jra.Entry(label_and_entry, bg="#faf3e0", font=self.font, justify='center', width=15)
        id_ss_entry.grid(row=0, column=1)
        name_ss_entry = jra.Entry(label_and_entry, bg="#faf3e0", font=self.font, justify='center', width=15)
        name_ss_entry.grid(row=1, column=1)

        packet_label = jra.Label(backup_box, bg="#faf3e0")
        confirm_button = jra.Button(packet_label, text="Save", bg="#eabf9f", width=10, height=1, font=self.font,
                                    command=lambda: self.let_save_session(duration, id_ss_entry.get(),
                                                                          name_ss_entry.get(), backup_box))
        confirm_button.grid(row=0, column=0, sticky="SW")
        cancel_button = jra.Button(packet_label, text="Cancel", bg="#eabf9f", width=10, height=1, font=self.font,
                                   command=backup_box.destroy)
        cancel_button.grid(row=0, column=1, sticky="SE")

        label_and_entry.grid(row=1, column=0, sticky="SE")
        packet_label.grid(row=2, column=0, sticky="S")
        id_ss_entry.focus_set()
        id_ss_entry.bind('<Return>',
                         lambda event: self.let_save_session(duration, id_ss_entry.get(), name_ss_entry.get(),
                                                             backup_box))
        name_ss_entry.bind('<Return>',
                           lambda event: self.let_save_session(duration, id_ss_entry.get(), name_ss_entry.get(),
                                                               backup_box))

    def add_all_user(self):
        # get employee photo
        current_unit = ""
        for temp_user in self.list_all_user:
            user_id = str(temp_user.ID)
            user_name = str(temp_user.name)
            num = 0
            found = False
            user_pic = Image.open("View/Stock/user-circle.png")
            while not found:
                if num > 100:
                    print("Wrong user picture! at", user_id)
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

            label = jra.Label(self.secondFrame, text=user_name, fg="#263942", font=self.font)
            if not current_unit.__eq__(temp_user.unit):
                self.column = 1
                self.row += 2
                unit_label = jra.Label(self.secondFrame, text=temp_user.unit, fg="#a13952", font='Helvetica 22 bold')
                unit_label.grid(row=self.row, column=self.column)
                self.list_unit_label.append(unit_label)
                self.column = 0
                self.row += 2
                current_unit = temp_user.unit
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
        if id_user in self.picked_user_IDs:
            self.picked_user_IDs.pop(self.picked_user_IDs.index(id_user))
            btn.configure(bg="#faf3e0")
        elif id_user not in self.picked_user_IDs:
            self.picked_user_IDs.append(id_user)
            btn.configure(bg="pink")
        else:
            print("Something wrong in pick employee")
        print(self.picked_user_IDs)

    def cancel_select(self):
        # hide this window
        self.master.withdraw()
        # reset for new session
        self.reset_data()
        # show up menuUI
        self.menuUI.controller.deiconify()

    def reset_data(self):
        # Un grid all image of old session
        for temp_button in self.list_unit_label:
            temp_button.grid_forget()
        for temp_button in self.list_buttons:
            temp_button.grid_forget()
        for temp_label in self.list_labels:
            temp_label.grid_forget()
        # Clear 2 old lists
        self.found_session = None
        self.picked_user_IDs.clear()
        self.string_selected_session.set("Select Your Session")

        self.list_all_user.clear()
        self.list_labels.clear()
        self.list_buttons.clear()
        self.list_images.clear()
        self.session_list.clear()

        # Set row and column 0 for new record session
        self.row = 0
        self.column = 0

    def load_all_session(self):
        temp_session_list = []
        with DataManager('Model/data/database/database.db') as db:
            all_session = db.get_all_session()
            for temp_sesion in all_session:
                temp_session_list.append(Session(*temp_sesion))
        print(temp_session_list.__len__(), " <-- num of session")
        self.session_list = temp_session_list

    def show(self, all_record_to_pick):
        self.load_all_session()
        self.reset_saved_sesions()
        self.list_all_user = ListEmployee(all_employee_data=all_record_to_pick)
        self.add_all_user()

        self.master.deiconify()

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

    def reset_saved_sesions(self):
        self.load_all_session()
        # change database here
        self.menu_option.delete(0, "end")
        for session in self.session_list:
            print(session.name)
            # set session.ID for trace after select in option menu
            self.menu_option.add_command(label=session.name,
                                         command=lambda value=session.ID: self.string_selected_session.set(value))
