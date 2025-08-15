import tkinter as tk
from PIL import ImageTk, ImageDraw
from ui.ui_preview_logic import generate_preview_pages

class PreviewPanel(tk.Frame):
    def __init__(self, parent, state):
        super().__init__(parent, bg="white", bd=2, relief="groove")
        self.state = state

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.inner_frame = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.image_refs = []

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def show_preview_from_state(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.image_refs.clear()

        try:
            pages = generate_preview_pages(self.state)
            for page in pages:
                border_color = (180, 180, 180)
                draw = ImageDraw.Draw(page)
                for i in range(3):
                    draw.rectangle([i, i, page.size[0]-1-i, page.size[1]-1-i], outline=border_color)

                preview_img = page.copy()
                preview_img.thumbnail((900, 1200))
                img_tk = ImageTk.PhotoImage(preview_img)

                frame = tk.Frame(self.inner_frame, bg="white")
                frame.pack(fill="x", pady=15)
                lbl = tk.Label(frame, image=img_tk, bg="white")
                lbl.pack(anchor="center")

                self.image_refs.append(img_tk)
        except Exception as e:
            print(f"Lỗi khi tạo preview: {e}")
