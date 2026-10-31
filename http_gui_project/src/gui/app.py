import tkinter as tk
from tkinter import ttk, messagebox
from .client_tab import ClientTab
from .server_tab import ServerTab

class App(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("HTTP-клиент и сервер"); self.geometry("1050x720"); self.minsize(820,560)
        notebook = ttk.Notebook(self); notebook.pack(fill="both", expand=True, padx=8, pady=8)
        self.client_tab = ClientTab(notebook); notebook.add(self.client_tab, text="Клиент")
        self.server_tab = ServerTab(notebook); notebook.add(self.server_tab, text="Сервер")
        notebook.add(self._about(notebook), text="О программе")
        self.protocol("WM_DELETE_WINDOW", self._close)
    def _about(self, parent):
        frame = ttk.Frame(parent, padding=20)
        ttk.Label(frame, text="HTTP-клиент и сервер на Python", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=8)
        ttk.Label(frame, text="Сеть реализована через socket и threading. Сторонние HTTP-клиенты и готовые серверные фреймворки не используются.", wraplength=800).pack(anchor="w")
        return frame
    def _close(self):
        self.server_tab.stop_server(); self.destroy()
