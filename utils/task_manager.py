import threading


def run_task(master, task, on_finish=None):
    def wrapper():
        try:
            result = task()
            if on_finish:
                master.after(0, lambda: on_finish(result))
        finally:
            master.after(0, lambda: master.progress_bar.set(0))
    threading.Thread(target=wrapper, daemon=True).start()