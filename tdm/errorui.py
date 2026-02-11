import sys
import tkinter as tk


def no_config_file_error():
    """Missing config.json next to the executable."""
    ui = tk.Tk()

    width = 320
    height = 140
    x = int((ui.winfo_screenwidth() / 2) - (width / 2))
    y = int((ui.winfo_screenheight() / 2) - (height / 2))
    ui.geometry(f"{width}x{height}+{x}+{y}")

    ui.title("tdm")
    ui.resizable(False, False)

    tk.Label(ui).pack()
    tk.Label(ui, text="Missing 'config.json'. Cannot start.").pack()
    tk.Label(ui, text="Please contact the administrator.").pack()
    tk.Label(ui).pack()

    def _exit_now():
        try:
            ui.destroy()
        finally:
            sys.exit(1)

    ui.protocol("WM_DELETE_WINDOW", _exit_now)
    button = tk.Button(ui, cursor="hand2", text="OK", width=15, command=_exit_now)
    button.pack()

    ui.mainloop()


def corrupted_config_file_error():
    """config.json is invalid or corrupted."""
    ui = tk.Tk()

    width = 320
    height = 140
    x = int((ui.winfo_screenwidth() / 2) - (width / 2))
    y = int((ui.winfo_screenheight() / 2) - (height / 2))
    ui.geometry(f"{width}x{height}+{x}+{y}")

    ui.title("tdm")
    ui.resizable(False, False)

    tk.Label(ui).pack()
    tk.Label(ui, text="'config.json' is corrupted. Cannot start.").pack()
    tk.Label(ui, text="Please contact the administrator.").pack()
    tk.Label(ui).pack()

    def _exit_now():
        try:
            ui.destroy()
        finally:
            sys.exit(1)

    ui.protocol("WM_DELETE_WINDOW", _exit_now)
    button = tk.Button(ui, cursor="hand2", text="OK", width=15, command=_exit_now)
    button.pack()

    ui.mainloop()
