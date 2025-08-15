import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
from PIL import Image, ImageEnhance
import tempfile
from tools.pdf_tools import export_to_pdf

# ===== STYLE CONFIG =====
BTN_BG = "#4CAF50"
BTN_HOVER = "#45a049"
TITLE_COLOR = "#2c3e50"
SECTION_BG = "#f7f9fa"
FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_SECTION = ("Segoe UI", 12, "bold")
FONT_BTN = ("Segoe UI", 11, "bold")

def create_toolbar(parent, state):
    toolbar = tk.Frame(parent, bg="#ffffff", width=250, bd=0)
    toolbar.pack_propagate(False)

    # Tiêu đề
    tk.Label(toolbar, text="📄 Tạo hồ sơ HKD/CTY", font=FONT_TITLE, fg=TITLE_COLOR, bg="#ffffff").pack(pady=(15, 20))

    # Các phần
    add_section(toolbar, "Giấy phép kinh doanh", [
        ("Chọn mặt trước", lambda: select_image(state, "license_front")),
        ("Chọn mặt sau", lambda: select_image(state, "license_back")),
    ])

    add_section(toolbar, "CCCD", [
        ("CCCD mặt trước", lambda: select_image(state, "cccd_front")),
        ("CCCD mặt sau", lambda: select_image(state, "cccd_back")),
    ])

    # Xuất PDF
    add_section(toolbar, "Xuất PDF")

    default_name = datetime.now().strftime("HS_%y_%m_%d_%H_%M")
    state["pdf_name_var"] = tk.StringVar(value=default_name)
    tk.Entry(toolbar, textvariable=state["pdf_name_var"], font=("Segoe UI", 10), relief="solid", bd=1).pack(pady=5, fill="x", padx=10)

    default_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(default_dir, exist_ok=True)
    state["save_dir_var"] = tk.StringVar(value=default_dir)

    path_frame = tk.Frame(toolbar, bg="#ffffff")
    path_frame.pack(pady=5, fill="x", padx=10)
    tk.Entry(path_frame, textvariable=state["save_dir_var"], relief="solid", bd=1).pack(side="left", fill="x", expand=True)
    tk.Button(path_frame, text="📂", command=lambda: choose_directory(state), relief="flat", bg="#ddd").pack(side="right", padx=2)

    # Nút xuất PDF
    create_button(toolbar, "📤 Tạo hồ sơ PDF", lambda: create_pdf(state)).pack(pady=20, fill="x", padx=10)

    return toolbar

def add_section(toolbar, title, buttons=None):
    frame = tk.Frame(toolbar, bg=SECTION_BG)
    frame.pack(fill="x", pady=(0, 5))
    tk.Label(frame, text=title, font=FONT_SECTION, bg=SECTION_BG, fg=TITLE_COLOR).pack(pady=8)

    if buttons:
        for text, cmd in buttons:
            create_button(toolbar, text, cmd).pack(pady=4, fill="x", padx=10)

def create_button(parent, text, command):
    btn = tk.Button(parent, text=text, bg=BTN_BG, fg="white", font=FONT_BTN, relief="flat", command=command, height=2, bd=0)
    btn.bind("<Enter>", lambda e: btn.config(bg=BTN_HOVER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BTN_BG))
    return btn

def choose_directory(state):
    folder = filedialog.askdirectory()
    if folder:
        state["save_dir_var"].set(folder)

def select_image(state, doc_key):
    file_path = filedialog.askopenfilename(
        title=f"Chọn {doc_key}",
        filetypes=[("Ảnh", "*.jpg;*.jpeg;*.png"), ("PDF", "*.pdf")]
    )
    if not file_path:
        return
    state["images"][doc_key] = file_path
    if file_path.lower().endswith((".jpg", ".jpeg", ".png")):
        img = Image.open(file_path).convert("L")
        img = ImageEnhance.Contrast(img).enhance(1.5)
        noir_path = os.path.join(tempfile.gettempdir(), f"{doc_key}_noir.png")
        img.save(noir_path)
        noir_key = doc_key + "_noir"
        if noir_key in state["images"]:
            state["images"][noir_key] = noir_path
    if "preview_panel" in state:
        state["preview_panel"].show_preview_from_state()

def create_pdf(state):
    pdf_name = state["pdf_name_var"].get() + ".pdf"
    save_path = os.path.join(state["save_dir_var"].get(), pdf_name)
    try:
        export_to_pdf(state, save_path, dpi=150, quality=80)
        messagebox.showinfo("Thành công", f"Hồ sơ đã tạo thành công:\n{save_path}")
        state["root"].destroy()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể tạo PDF:\n{e}")
