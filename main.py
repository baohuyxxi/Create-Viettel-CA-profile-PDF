import tkinter as tk
from ui.ui_toolbar import create_toolbar
from ui.ui_preview import PreviewPanel
from tools.signature_utils import load_signature_image

def start_app(state):
    root = tk.Tk()
    root.title("Tạo hồ sơ PDF")
    root.geometry("1200x800")
    root.configure(bg="white")
    state["root"] = root

    toolbar = create_toolbar(root, state)
    toolbar.pack(side="left", fill="y")

    preview_panel = PreviewPanel(root, state)
    preview_panel.pack(side="right", fill="both", expand=True)
    state["preview_panel"] = preview_panel

    root.mainloop()

if __name__ == "__main__":
    state = {
        "images": {
            "license_front": None,
            "license_back": None,
            "license_front_noir": None,
            "license_back_noir": None,
            "cccd_front": None,
            "cccd_back": None,
            "cccd_front_noir": None,
            "cccd_back_noir": None
        },
        "signature_path": load_signature_image(),
        "root": None,
    }
    start_app(state)
