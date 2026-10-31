import json, queue, threading, tkinter as tk
from tkinter import ttk
from ..client.http_client import HttpClient

class ClientTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10); self.result_queue = queue.Queue(); self.client = HttpClient()
        self.url = tk.StringVar(value="http://example.com/"); self.method = tk.StringVar(value="GET"); self.loading = tk.StringVar(value="Готово")
        ttk.Label(self, text="URL:").grid(row=0,column=0,sticky="w")
        ttk.Entry(self, textvariable=self.url).grid(row=0,column=1,columnspan=4,sticky="ew",padx=5,pady=3)
        ttk.Label(self,text="Метод:").grid(row=1,column=0,sticky="w")
        combo=ttk.Combobox(self,textvariable=self.method,values=("GET","POST"),state="readonly",width=10); combo.grid(row=1,column=1,sticky="w",padx=5)
        combo.bind("<<ComboboxSelected>>", lambda _e:self._toggle_body())
        ttk.Label(self,text="Заголовки (имя: значение, по одному на строку):").grid(row=2,column=0,columnspan=5,sticky="w",pady=(8,0))
        self.headers=tk.Text(self,height=4,wrap="none"); self.headers.grid(row=3,column=0,columnspan=5,sticky="ew",pady=3)
        ttk.Label(self,text="Тело POST:").grid(row=4,column=0,columnspan=5,sticky="w")
        self.body=tk.Text(self,height=5,wrap="word"); self.body.grid(row=5,column=0,columnspan=5,sticky="ew",pady=3)
        buttons=ttk.Frame(self); buttons.grid(row=6,column=0,columnspan=5,sticky="w",pady=4)
        ttk.Button(buttons,text="Отправить",command=self.send).pack(side="left",padx=(0,5)); ttk.Button(buttons,text="Очистить",command=self.clear).pack(side="left",padx=5)
        ttk.Label(buttons,textvariable=self.loading).pack(side="left",padx=12)
        ttk.Label(self,text="Ответ (статус, заголовки, тело):").grid(row=7,column=0,columnspan=5,sticky="w",pady=(8,0))
        self.output=tk.Text(self,wrap="word",state="disabled"); self.output.grid(row=8,column=0,columnspan=5,sticky="nsew",pady=3)
        self.columnconfigure(1,weight=1); self.columnconfigure(2,weight=1); self.rowconfigure(8,weight=1); self._toggle_body(); self.after(100,self._poll)
    def _toggle_body(self): self.body.configure(state="normal" if self.method.get()=="POST" else "disabled")
    def _headers(self):
        result={}
        for line in self.headers.get("1.0","end").splitlines():
            if not line.strip(): continue
            if ":" not in line: raise ValueError(f"Заголовок должен иметь вид имя: значение — {line}")
            key,value=line.split(":",1)
            if not key.strip(): raise ValueError("Имя заголовка не может быть пустым")
            result[key.strip()]=value.strip()
        return result
    def send(self):
        try:
            url=self.url.get().strip(); headers=self._headers(); method=self.method.get(); body=self.body.get("1.0","end-1c").encode("utf-8")
            if not url: raise ValueError("Введите URL")
        except Exception as exc: self._show(f"Ошибка ввода: {exc}"); return
        self.loading.set("Отправка...")
        threading.Thread(target=self._worker,args=(method,url,headers,body),daemon=True).start()
    def _worker(self,method,url,headers,body):
        try:
            response=self.client.get(url,headers) if method=="GET" else self.client.post(url,body,"text/plain; charset=utf-8",headers)
            try: text=response.body.decode("utf-8")
            except UnicodeDecodeError: text=response.body.decode("iso-8859-1",errors="replace")
            result=f"Статус: {response.status} {response.reason}\n\nЗаголовки:\n"+"".join(f"{k}: {v}\n" for k,v in response.headers.items())+f"\nТело:\n{text}"
            self.result_queue.put((result,None))
        except Exception as exc: self.result_queue.put((None,f"{type(exc).__name__}: {exc}"))
    def _poll(self):
        try:
            while True:
                result,error=self.result_queue.get_nowait(); self.loading.set("Ошибка" if error else "Готово"); self._show(error or result)
        except queue.Empty: pass
        if self.winfo_exists(): self.after(100,self._poll)
    def _show(self,text):
        self.output.configure(state="normal"); self.output.delete("1.0","end"); self.output.insert("1.0",text); self.output.configure(state="disabled")
    def clear(self):
        self.headers.delete("1.0","end"); self.body.configure(state="normal"); self.body.delete("1.0","end"); self._show(""); self.loading.set("Готово"); self._toggle_body()
