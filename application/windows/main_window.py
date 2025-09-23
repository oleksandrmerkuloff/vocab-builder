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
    """Main Window for all app includes widgets and starting functions"""
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

        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.pack(pady=(10, 0))
        self.progress_bar.set(0)
        self.progress_bar.stop()

        self.progress_label = ctk.CTkLabel(
            self,
            text='0/0',
            font=('Roboto', 14)
            )
        self.progress_label.pack()

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
            pady=(25, 10),
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
        """Check value of checkboxes and start one of the processes"""
        if self.card_checkbox.get() and self.translation_checkbox.get():
            self.translation_and_cards()
        elif self.card_checkbox.get():
            self.cards_gen_process()
        elif self.translation_checkbox.get():
            self.translation_process()

    def uncheck(self):
        """Deselect checkboxes"""
        self.card_checkbox.deselect()
        self.translation_checkbox.deselect()

    def cards_gen_process(self) -> None:
        """Gets path for txt and pdf files and start process of card gen"""
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

        if not datafile_path or not card_file_path:
            return

        def task():
            self.progress_bar.set(0)
            create_pdf(self, datafile_path, card_file_path)
            self.progress_bar.set(1)

        threading.Thread(target=task, daemon=True).start()

    def translation_process(self) -> None:
        """Gets sourcefile path for translation process"""
        self.uncheck()
        filepath = askopenfilename(
            parent=self,
            title='Open File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )

        if not filepath:
            return

        def task():
            self.after(0, lambda: self.progress_bar.set(0))

            async def runner():
                await get_words(self, filepath, MainWindow.create_to_learn_file)

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(runner())
            loop.close()

            self.after(0, lambda: self.progress_bar.set(1))
        threading.Thread(target=task, daemon=True).start()

    def translation_and_cards(self) -> None:
        """Start point func for translation and cards generation"""
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

        if not save_pdf or not save_txt or not filepath:
            return

        def task():
            self.after(0, lambda: self.progress_bar.set(0))

            async def runner():
                def after_translate(master, storage):
                    with open(save_txt, 'w', encoding='utf-8') as f:
                        for word in storage:
                            f.write(f'Freq: {word[2]}; {word[0]} - {word[1]}\n')
                    create_pdf(master, save_txt, save_pdf)
                    self.after(0, lambda: self.progress_bar.set(1))

                await get_words(self, filepath, after_translate)

            asyncio.run(runner())

        threading.Thread(target=task, daemon=True).start()

    @staticmethod
    def create_to_learn_file(master: Any, storage: list) -> None:
        """Create result txt file with words translation"""
        file = asksaveasfilename(
            parent=master,
            title='Save File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt'),],
            defaultextension='.txt',
        )
        if not file:
            return
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
