import os
import glob
import sys

def resource_path(relative_path):
    """Lấy đường dẫn thật khi chạy exe hoặc code gốc"""
    try:
        base_path = sys._MEIPASS  # Khi chạy từ exe
    except AttributeError:
        base_path = os.path.abspath(".")  # Khi chạy code gốc
    return os.path.join(base_path, relative_path)

def load_signature_image():
    sig_folder = resource_path("signatures")
    exts = ("*.png", "*.jpg", "*.jpeg")
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(sig_folder, ext)))
    if files:
        return files[0]  # Lấy file ảnh chữ ký đầu tiên tìm được
    return None
