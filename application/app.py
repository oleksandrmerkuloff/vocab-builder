import customtkinter as ctk

from application.windows.main_window import MainWindow


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Learn English Dude')
        self.geometry('720x480')
        self.resizable(False, False)

        self.main_window = MainWindow(self)
