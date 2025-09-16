import customtkinter as ctk
from googletrans import Translator

import os
import asyncio
import threading
from string import punctuation
import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfile


BASE_DIR = os.getcwd()


class App(ctk.CTk):
    def __init__(self):
        # Word file info
        # Design config

        super().__init__()
        self.geometry('720x480')
        self.title('Learn English Dude')
        self.resizable(False, False)

        self.load_file_btn = ctk.CTkButton(
            self,
            text='Load File',
            command=self.load_file,
            width=200,
            height=100,
            font=('Times New Roman', 28,)
        )
        self.load_file_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    @staticmethod
    async def translate_one(word: str) -> str:
        async with Translator() as translator:
            result = await translator.translate(word, dest='ru', src='en')
            return result.text

    @staticmethod
    async def translate_words(words):
        tasks = [App.translate_one(w) for w in words]
        translations = await asyncio.gather(*tasks, return_exceptions=True)
        return translations

    def report_window(self, words=None):
        window = ctk.CTkToplevel(
                self
            )
        window.resizable(False, False)
        window.title('Report')
        window.geometry('600x400')
        if words:
            report_label = ctk.CTkLabel(
                window,
                text=f'Find unique words: {words}.\nFile was saved.',
                font=('Times New Roman', 28,)
            )
        else:
            report_label = ctk.CTkLabel(
                window,
                text='Operation failed. Try again.',
                font=('Times New Roman', 28,)
            )
        report_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def load_file(self):
        file = askopenfile(
            parent=self,
            title='Open File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt')]
        )
        return self.get_words(file.name)

    def get_words(self, file):
        try:
            with open(file, 'r') as file:
                translator = str.maketrans('', '', punctuation)
                splitted_file = file.read().translate(translator).split()
                unique_words = [
                    x.lower() for x in splitted_file
                    if not x.isdigit()
                    ]
                return self.create_to_learn_file(list(set(unique_words)))
        except FileExistsError:
            raise FileExistsError('File doesn\'t exists.\nTry Again!')
        except FileNotFoundError:
            raise FileNotFoundError('Wrong path for file.\nTry Again!')

    def create_to_learn_file(self, words):
        file = asksaveasfile(
            parent=self,
            mode='w',
            title='Save File',
            initialdir=BASE_DIR,
            filetypes=[('Text files', '.*txt'),],
            defaultextension='.txt'
        )
        if file:
            def writing():
                data_for_file = ''
                translations = asyncio.run(App.translate_words(words))
                for word in range(len(words)):
                    data_for_file += words[word] + ' - ' + translations[word] + '\n'

                file.write(data_for_file.strip())
                file.close()

                self.report_window(len(words))
            threading.Thread(target=writing, daemon=True).start()
        else:
            self.report_window()
