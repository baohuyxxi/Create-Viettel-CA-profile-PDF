from PIL import Image, ImageEnhance

DPI = 300
def mm_to_px(mm, dpi=DPI):
    return int((mm / 25.4) * dpi)

def resize_image_to_mm(image_path, width_mm, height_mm, keep_alpha=False):
    mode = "RGBA" if keep_alpha else "RGB"
    img = Image.open(image_path).convert(mode)
    img = img.resize((mm_to_px(width_mm), mm_to_px(height_mm)), Image.LANCZOS)
    return img


def overlay(base_img, overlay_img, pos):
    base_img.paste(overlay_img, pos, overlay_img)
    return base_img

