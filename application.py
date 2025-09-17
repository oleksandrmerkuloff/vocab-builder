import customtkinter as ctk
from googletrans import Translator

import os
import asyncio
import threading
from string import punctuation
import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename


BASE_DIR = os.getcwd()


class App(ctk.CTk):
    def __init__(self):
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

    async def translate_words(self, unique_words, all_words):
        async with Translator() as translator:
            tasks = [translator.translate(word, dest='ru', src='en') for word in unique_words]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            storage = []
            for word, res in zip(unique_words, results):
                if isinstance(res, Exception):
                    storage.append([word, f"[error: {type(res).__name__}]", str(all_words.count(word))])
                else:
                    storage.append([word, res.text, str(all_words.count(word))])
            return storage

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
        threading.Thread(target=self.get_words, args=(file.name,), daemon=True).start()

    def get_words(self, file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                translator = str.maketrans('', '', punctuation)
                splitted_file = f.read().translate(translator).split()
                words = [w.lower() for w in splitted_file if not w.isdigit()]
                unique_words = set(words)

            storage = asyncio.run(self.translate_words(unique_words, words))
            self.after(0, lambda: self.create_to_learn_file(storage))
        except FileExistsError:
            raise FileExistsError('File doesn\'t exists.\nTry Again!')
        except FileNotFoundError:
            raise FileNotFoundError('Wrong path for file.\nTry Again!')

    def create_to_learn_file(self, storage: list):
        file = asksaveasfilename(
            parent=self,
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
                self.report_window(len(storage))
            except TypeError:
                self.report_window()
        else:
            self.report_window()
