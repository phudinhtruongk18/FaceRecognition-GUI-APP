import Controller.Program as ProgramUI
import tkinter as tk

if __name__ == '__main__':
    app = ProgramUI.MainUI()
    app.iconphoto(False, tk.PhotoImage(file='View/Stock/icon.ico'))
    app.mainloop()
