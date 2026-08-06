"""
model_downloader.py
--------------------
مدل GGUF معمولاً چند صد مگابایت تا چند گیگابایت است و گنجاندنش داخل APK
منطقی نیست (محدودیت مارکت‌ها و حجم دانلود اولیه). راه‌حل استاندارد همان
کاری‌ست که اپ‌هایی مثل PocketPal/MLC Chat انجام می‌دهند: مدل فقط در اولین
اجرا و فقط یک‌بار دانلود می‌شود؛ از آن به بعد اپ ۱۰۰٪ آفلاین کار می‌کند.
"""

import os
import threading
import requests

# لینک مستقیم یک مدل کوچک و باکیفیت (قابل تغییر به هر مدل GGUF دیگر)
DEFAULT_MODEL_URL = (
    "https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/"
    "qwen2.5-3b-instruct-q4_k_m.gguf"
)


def download_model(dest_path: str, url: str = DEFAULT_MODEL_URL,
                    on_progress=None, on_done=None, on_error=None):
    """دانلود را در یک ترد جدا اجرا می‌کند تا رابط کاربری فریز نشود.

    on_progress(fraction: float) در حین دانلود صدا زده می‌شود.
    on_done() بعد از موفقیت.
    on_error(str) در صورت خطا.
    """

    def _run():
        tmp_path = dest_path + ".part"
        try:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with requests.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0)) or None
                downloaded = 0
                with open(tmp_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024 * 512):
                        if not chunk:
                            continue
                        f.write(chunk)
                        downloaded += len(chunk)
                        if on_progress and total:
                            on_progress(downloaded / total)
            os.replace(tmp_path, dest_path)
            if on_done:
                on_done()
        except Exception as exc:  # noqa: BLE001
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            if on_error:
                on_error(str(exc))

    threading.Thread(target=_run, daemon=True).start()
