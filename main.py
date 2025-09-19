import os, sys

from application.app import App


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):  # коли запускається .exe
        os.add_dll_directory(os.path.dirname(sys.executable))
    app = App()
    app.mainloop()
