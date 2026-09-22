import tkinter as tk
from tkinter import ttk

def start_progress(next_screen):

    splash = tk.Tk()
    splash.title("Loading")
    splash.attributes('-fullscreen', True)
    splash.configure(bg="#1e1e1e")

    frame = tk.Frame(splash, bg="#1e1e1e")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(frame,
        text="Dropout Risk Prediction System",
        font=("Helvetica", 26, "bold"),
        fg="white",
        bg="#1e1e1e").pack(pady=20)

    progress = ttk.Progressbar(frame, length=500)
    progress.pack(pady=20)

    lbl = tk.Label(frame, text="0%", fg="white", bg="#1e1e1e")
    lbl.pack()

    def auto():
        v = progress['value']
        if v < 100:
            v += 1
            progress['value'] = v
            lbl.config(text=str(v)+"%")
            splash.after(30, auto)
        else:
            splash.destroy()
            next_screen()

    splash.after(300, auto)
    splash.mainloop()
