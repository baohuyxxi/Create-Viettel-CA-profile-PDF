from pdf2image import convert_from_path
from tools.tool_image import resize_image_to_mm, mm_to_px, overlay
from PIL import Image

def generate_preview_pages(state):
    imgs = state["images"]
    pages = []

    if imgs["license_back"]:
        # Có mặt sau
        order = [
            imgs["license_front"],
            imgs["license_back"],
            imgs["license_front_noir"],
            imgs["license_back_noir"],
            (imgs["cccd_front"], imgs["cccd_back"], imgs["cccd_front_noir"], imgs["cccd_back_noir"])
        ]
    else:
        # Không có mặt sau
        order = [
            imgs["license_front"],
            imgs["license_front_noir"],
            (imgs["cccd_front"], imgs["cccd_back"], imgs["cccd_front_noir"], imgs["cccd_back_noir"])
        ]
    for item in order:
        if isinstance(item, tuple):
            # Trang 4 ảnh CCCD
            page = Image.new("RGB", (mm_to_px(210), mm_to_px(297)), (255, 255, 255))
            margin_mm = 2
            img_width_mm = 104
            img_height_mm = 63
            margin_px = mm_to_px(margin_mm)
            w_small = mm_to_px(img_width_mm)
            h_small = mm_to_px(img_height_mm)

            positions = [
                (margin_px, margin_px),
                (w_small + margin_px * 2, margin_px),
                (margin_px, h_small + margin_px * 2),
                (w_small + margin_px * 2, h_small + margin_px * 2)
            ]
            for img_path, pos in zip(item, positions):
                if img_path:
                    small_img = resize_image_to_mm(img_path, img_width_mm, img_height_mm)
                    page.paste(small_img, pos)
            overlay_img = resize_image_to_mm(state["signature_path"], 125, 50, keep_alpha=True)
            pos_x = mm_to_px(210 / 5)
            pos_y = mm_to_px(297/2.2)
            page = overlay(page, overlay_img, (pos_x, pos_y))
            pages.append(page)
        else:
            if item:
                page = resize_image_to_mm(item, 210, 297)
                if item == imgs["license_front_noir"]:
                    # Nếu là bản noir, chèn chữ ký
                    overlay_img = resize_image_to_mm(state["signature_path"], 100, 40, keep_alpha=True)
                    pos_x = mm_to_px(210 / 10)
                    pos_y = mm_to_px(297 - 297 / 4 + 5)
                    if imgs["license_back"]:
                       pos_y = mm_to_px(297 - 297/ 7)
                    page = overlay(page, overlay_img, (pos_x, pos_y))
                if item == imgs["license_back_noir"]:
                    overlay_img = resize_image_to_mm(state["signature_path"], 100, 40, keep_alpha=True)
                    pos_x = mm_to_px(210 / 11)
                    pos_y = mm_to_px(297/3 )
                    page = overlay(page, overlay_img, (pos_x, pos_y))
                pages.append(page)
               

    return pages