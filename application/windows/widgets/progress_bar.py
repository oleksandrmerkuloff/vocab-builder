from customtkinter import CTkProgressBar


class CustomProgressBar(CTkProgressBar):
    def __init__(self, master: Any, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.refresh()

    def refresh(self) -> None:
        self.set(0)
