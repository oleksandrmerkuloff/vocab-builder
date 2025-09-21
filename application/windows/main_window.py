import customtkinter as ctk
from customtkinter import CTkFrame
from tkinter.filedialog import askopenfilename, asksaveasfilename

import os
import asyncio
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
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)
        self.progress_bar.stop()

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
            text='Generate cards',
            font=('Roboto', 28)
        )
        self.card_checkbox.pack(
            pady=(50, 10),
            padx=(45, 0),
            anchor='w'
        )

        self.translation_checkbox = ctk.CTkCheckBox(
            self,
            text='Translate words',
            font=('Roboto', 28)
        )
        self.translation_checkbox.pack(
            pady=(50, 10),
            padx=(45, 0),
            anchor='w'
        )

        self.load_file_button = LoadFileButton(
            self,
            command=self.start_operation
            )
        self.load_file_button.pack(
            pady=(20, 40),
            side='bottom'
        )

    def start_operation(self):
        if self.card_checkbox.get() and self.translation_checkbox.get():
            self.translation_and_cards()
        elif self.card_checkbox.get():
            self.cards_gen_process()
        elif self.translation_checkbox.get():
            self.translation_process()

    def uncheck(self):
        self.card_checkbox.deselect()
        self.translation_checkbox.deselect()

    def cards_gen_process(self):
        self.uncheck()
        datafile_path = askopenfilename(
            parent=self,
            title='Open File With Words',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )
        card_file_path = asksaveasfilename(
            parent=self,
            title='Save File With Cards',
            initialdir=BASE_DIR,
            filetypes=[('Portable Document Format', '.*pdf'),],
            defaultextension='.pdf',
        )

        def task():
            self.progress_bar.set(0)
            create_pdf(self, datafile_path, card_file_path)
            self.progress_bar.set(1)

        threading.Thread(target=task, daemon=True).start()

    def translation_process(self):
        self.uncheck()
        filepath = askopenfilename(
            parent=self,
            title='Open File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )

        def task():
            self.progress_bar.set(0)
            asyncio.run(get_words(self, filepath, MainWindow.create_to_learn_file))
            self.progress_bar.set(1)

        threading.Thread(target=task, daemon=True).start()

    def translation_and_cards(self):
        self.uncheck()
        filepath = askopenfilename(
            parent=self,
            title='Open File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )
        save_txt = asksaveasfilename(
            parent=self,
            title='Save Translated Words',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')],
            defaultextension='.txt',
        )
        save_pdf = asksaveasfilename(
            parent=self,
            title='Save Cards PDF',
            initialdir=BASE_DIR,
            filetypes=[('Portable Document Format', '.*pdf')],
            defaultextension='.pdf',
        )

        def task():
            self.after(0, lambda: self.progress_bar.set(0))

            async def runner():
                async def after_translate(master, storage):
                    with open(save_txt, 'w', encoding='utf-8') as f:
                        for word in storage:
                            f.write(f'Freq: {word[2]}; {word[0]} - {word[1]}\n')
                    create_pdf(master, save_txt, save_pdf)
                    self.progress_bar.set(1)
                    self.after(0, lambda: ReportWindow(master=self, c_text="Translate + PDF Ready"))

                await get_words(self, filepath, after_translate)
            asyncio.run(runner())
        threading.Thread(target=task, daemon=True).start()

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
                words_counter = str(len(storage))
                ReportWindow(master=master, amount_of_words=words_counter)
            except TypeError:
                ReportWindow(master=master)
        else:
            ReportWindow(master=master)
