import customtkinter as ctk

import tkinter as tk


class ReportWindow(ctk.CTkToplevel):
    def __init__(
        self,
        amount_of_words: str | None = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title('Report Window')
        self.geometry('600x400')
        self.resizable(False, False)

        # widgets
        if amount_of_words:
            report_label = ctk.CTkLabel(
                self,
                text=f'Find unique words: {amount_of_words}.\nFile was saved.',
                font=('Times New Roman', 28,)
            )
        else:
            report_label = ctk.CTkLabel(
                amount_of_words,
                text='Operation failed. Try again.',
                font=('Times New Roman', 28,)
            )
        report_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
