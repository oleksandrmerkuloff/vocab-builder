import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.filedialog import askopenfilename, asksaveasfilename

import os
import threading
from typing import Any

from application.windows.report import ReportWindow
from application.windows.widgets.buttons import LoadFileButton
from utils.wordsmith import get_words
from utils.word_card import create_pdf


BASE_DIR = os.getcwd()


class MainWindow(CTkFrame):
    def __init__(self, master: Any, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.pack(fill='both', expand=True)

        # Widgets

        self.welcome_label = ctk.CTkLabel(
            self,
            text="""Hello Illya!\n
            I suppose this app helps you improve your English:)
            """,
            font=('Roboto', 26),
            justify='center'
        )
        self.welcome_label.pack(
            pady=(20, 10),
            anchor='n'
        )

        self.card_checkbox = ctk.CTkCheckBox(
            self,
            text='Generate cards?',
            font=('Roboto', 28)
        )
        self.card_checkbox.pack(
            pady=(50, 10),
            padx=(45, 0),
            anchor='w'
        )

        self.load_file_button = LoadFileButton(self, command=self.load_file)
        self.load_file_button.pack(
            pady=(20, 40),
            side='bottom'
        )

    def load_file(self):
        cards = self.card_checkbox.get()
        self.card_checkbox.deselect()
        filepath = askopenfilename(
            parent=self,
            title='Open File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )
        threading.Thread(
            target=get_words,
            args=(self, filepath, MainWindow.create_to_learn_file, cards),
            daemon=True).start()

    @staticmethod
    def create_to_learn_file(master: Any, storage: list, cards: int):
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
                if cards:
                    MainWindow.generate_cards(master, storage)
                words_counter = str(len(storage))
                ReportWindow(master=master, amount_of_words=words_counter)
            except TypeError:
                ReportWindow(master=master)
        else:
            ReportWindow(master=master)

    @staticmethod
    def generate_cards(master, words: list) -> None:
        file = asksaveasfilename(
            parent=master,
            title='Save File With Cards',
            initialdir=BASE_DIR,
            filetypes=[('Portable Document Format', '.*pdf'),],
            defaultextension='.pdf',
        )
        return create_pdf(words, file)
