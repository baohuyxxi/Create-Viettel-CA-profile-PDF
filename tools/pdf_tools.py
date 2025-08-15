
from PIL import Image

from ui.ui_preview import generate_preview_pages

DPI = 300




def export_to_pdf(state, output_path, dpi=150, quality=85):
    """Xuất file PDF dung lượng nhỏ."""
    try:
        pages = generate_preview_pages(state)
        if not pages:
            print("Không có trang nào để xuất.")
            return

        # Chuyển tất cả ảnh sang RGB + resize giảm DPI
        new_pages = []
        for page in pages:
            page_rgb = page.convert("RGB")
            if dpi < DPI:
                new_w = int(page.width * dpi / DPI)
                new_h = int(page.height * dpi / DPI)
                page_rgb = page_rgb.resize((new_w, new_h), Image.LANCZOS)
            new_pages.append(page_rgb)

        first_page, *rest_pages = new_pages
        first_page.save(
            output_path,
            "PDF",
            resolution=dpi,
            quality=quality,  # JPEG quality khi nén
            optimize=True,
            save_all=True,
            append_images=rest_pages
        )
        print(f"✅ Xuất PDF thành công: {output_path}")
    except Exception as e:
        print(f"❌ Lỗi khi xuất PDF: {e}")
