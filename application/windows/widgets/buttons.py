from typing import Any
from customtkinter import CTkButton


class LoadFileButton(CTkButton):
    """Load Button Class"""
    def __init__(self, master: Any, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(
            text='Load File',
            anchor='center',
            hover=True,
            width=650,
            height=60,
            font=('Roboto', 26,)
        )
