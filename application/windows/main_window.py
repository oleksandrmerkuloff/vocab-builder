import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.filedialog import askopenfilename, asksaveasfilename

import os
import threading
from typing import Any

from application.windows.report import ReportWindow
from application.windows.widgets.buttons import LoadFileButton
from utils.wordsmith import get_words


BASE_DIR = os.getcwd()


class MainWindow(CTkFrame):
    def __init__(self, master: Any, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(fill='both', expand=True)

        self.welcome_label = ctk.CTkLabel(
            self,
            text="""Hello Illya!\n
            I suppose this app helps you improve your English:)
            """,
            font=('Roboto', 28)
        )
        self.welcome_label.pack()

        self.load_file_button = LoadFileButton(self, command=self.load_file)
        self.load_file_button.pack()

    def load_file(self):
        filepath = askopenfilename(
            parent=self,
            title='Open File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )
        threading.Thread(
            target=get_words,
            args=(self, filepath, MainWindow.create_to_learn_file),
            daemon=True).start()

    @staticmethod
    def create_to_learn_file(master: Any, storage: list):
        file = asksaveasfilename(
            parent=master,
            title='Save File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt'),],
            defaultextension='.txt',
        )
        if file:
            try:
                to_file = ''
                for word in storage:
                    text = (
                        f'Freq: {word[2]}; '
                        f'{word[0]} - {word[1]}\n'
                            )
                    to_file += text
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(to_file)
                print('done')
                words_counter = str(len(storage))
                ReportWindow(master=master, amount_of_words=words_counter)
            except TypeError:
                ReportWindow(master=master)
        else:
            ReportWindow(master=master)
