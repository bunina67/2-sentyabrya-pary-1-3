import logging
from pathlib import Path
from .gui.app import App

def configure_logging():
    log_path=Path("http_gui.log")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", handlers=[logging.FileHandler(log_path,encoding="utf-8"), logging.StreamHandler()])

if __name__ == "__main__":
    configure_logging(); App().mainloop()
