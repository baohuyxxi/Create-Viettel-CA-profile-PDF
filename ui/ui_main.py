import tkinter as tk
from ui.ui_toolbar import create_toolbar
from ui.ui_preview import PreviewPanel

def start_app(state):
    root = tk.Tk()
    root.title("Phần mềm xử lý hồ sơ")
    root.geometry("1200x800")
    root.configure(bg="#f4f6f8")
    state["root"] = root

    # Main frame chia 2 phần: toolbar + preview
    main_frame = tk.Frame(root, bg="#f4f6f8")
    main_frame.pack(fill="both", expand=True)

    # Toolbar bên trái
    toolbar_frame = create_toolbar(main_frame, state)
    toolbar_frame.pack(side="left", fill="y", padx=10, pady=10)

    # Preview bên phải
    preview_panel = PreviewPanel(main_frame, state)
    preview_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    state["preview_panel"] = preview_panel

    root.mainloop()
