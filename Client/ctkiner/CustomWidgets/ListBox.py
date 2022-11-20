import tkinter as tk
import customtkinter as ctk

import sv_ttk

class ListBox(ctk.CTkFrame):
    def __init__(self, parent: ctk.CTk, name, debug=False, height: int = 200, width: int = 200):
        ctk.CTkFrame.__init__(self, parent)  # , height=parent.winfo_height(),
        self.config(height=height)
        self.config(width=width)

        print('label')

    def add_frame(self, name):
        friend_frame = ctk.CTkFrame(self, height=50, width=190, borderwidth=0, border=0,
                                    border_width=0)
        name_label = ctk.CTkLabel(friend_frame, text=name, width=180, height=50)
        name_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        friend_frame.grid()


class CustomWidget(tk.Frame):
    def __init__(self, parent, label, default=""):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text=label, anchor="w")
        self.entry = tk.Entry(self)
        self.entry.insert(0, default)

        self.label.pack(side="top", fill="x")
        self.entry.pack(side="bottom", fill="x", padx=4)

    def get(self):
        return self.entry.get()
