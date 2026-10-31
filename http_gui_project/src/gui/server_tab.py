import logging, queue, tkinter as tk, webbrowser
from tkinter import ttk, messagebox
from ..server.http_server import HttpServer

class ServerTab(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent,padding=10); self.events=queue.Queue(); self.port=tk.StringVar(value="8080"); self.state=tk.StringVar(value="Остановлен")
        self.logger=logging.getLogger("http_gui")
        self.server=HttpServer(on_log=self.events.put)
        top=ttk.Frame(self); top.pack(fill="x")
        ttk.Label(top,text="Порт:").pack(side="left"); ttk.Entry(top,textvariable=self.port,width=10).pack(side="left",padx=5)
        ttk.Button(top,text="Запустить",command=self.start_server).pack(side="left",padx=4); ttk.Button(top,text="Остановить",command=self.stop_server).pack(side="left",padx=4)
        ttk.Label(top,text="Состояние:").pack(side="left",padx=(15,4)); self.state_label=ttk.Label(top,textvariable=self.state,foreground="red"); self.state_label.pack(side="left")
        ttk.Button(top,text="Открыть в браузере",command=self.open_browser).pack(side="right")
        cols=("time","method","path","status","ms"); self.tree=ttk.Treeview(self,columns=cols,show="headings",height=20)
        for col,label,width in (("time","Время",90),("method","Метод",90),("path","Путь",360),("status","Статус",90),("ms","мс",100)):
            self.tree.heading(col,text=label); self.tree.column(col,width=width,anchor="w")
        self.tree.pack(fill="both",expand=True,pady=10); ttk.Button(self,text="Очистить лог",command=self.clear_log).pack(anchor="e")
        self.after(100,self._poll)
    def start_server(self):
        try:
            port=int(self.port.get())
            if not 1<=port<=65535: raise ValueError("Порт должен быть в диапазоне 1–65535")
            self.server.start(port=port); self.state.set(f"Запущен на {port}"); self.state_label.configure(foreground="green")
        except Exception as exc: messagebox.showerror("Не удалось запустить сервер",str(exc))
    def stop_server(self):
        self.server.stop(); self.state.set("Остановлен"); self.state_label.configure(foreground="red")
    def open_browser(self): webbrowser.open(f"http://127.0.0.1:{self.server.port}/")
    def clear_log(self):
        for item in self.tree.get_children(): self.tree.delete(item)
    def _poll(self):
        try:
            while True:
                event=self.events.get_nowait(); self.tree.insert("","end",values=(event["time"],event["method"],event["path"],event["status"],event["ms"]))
        except queue.Empty: pass
        if self.winfo_exists(): self.after(100,self._poll)
