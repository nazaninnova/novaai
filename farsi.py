"""
farsi.py
--------
Kivy به‌صورت پیش‌فرض حروف فارسی/عربی را به‌هم نمی‌چسباند (shaping) و
جهت راست‌به‌چپ را هم رعایت نمی‌کند. این ماژول متن فارسی را قبل از
نمایش، «آماده‌ی نمایش» می‌کند.

نصب لازم:
    pip install arabic-reshaper python-bidi
"""

import arabic_reshaper
from bidi.algorithm import get_display

_reshaper_config = arabic_reshaper.config_for_true_type_font(
    None, arabic_reshaper.ENABLE_ALL_LIGATURES
) if False else None  # تنظیم پیش‌فرض کافی است

_reshaper = arabic_reshaper.ArabicReshaper()


def rtl(text: str) -> str:
    """متن فارسی را برای نمایش صحیح در Label/Button آماده می‌کند.

    هر خط را جداگانه پردازش می‌کنیم چون اجرای bidi روی کل یک متن
    چندخطی/چندپاراگرافی یکجا، ترتیب خط‌ها و پاراگراف‌ها را به‌هم می‌ریزد.
    """
    if not text:
        return text
    try:
        lines = text.split("\n")
        processed = []
        for line in lines:
            if line.strip():
                reshaped = _reshaper.reshape(line)
                processed.append(get_display(reshaped))
            else:
                processed.append(line)
        return "\n".join(processed)
    except Exception:  # noqa: BLE001
        return text


def wrap_rtl(text: str, max_chars: int = 26) -> str:
    """مخصوص متن‌های طولانی (مثل جواب هوش مصنوعی) که قرار است داخل یک
    Label با عرض محدود نمایش داده شوند.

    مشکل: اگر بگذاریم خود Kivy متن را به‌صورت خودکار بشکند، این کار را
    روی متنِ از قبل بازآرایی‌شده (bidi) انجام می‌دهد و چون Label فرض
    می‌کند متن چپ‌به‌راست است، نقطه‌ی شکستن خط را اشتباه انتخاب می‌کند و
    ترتیب کلمات بهم می‌ریزد (همان مشکلی که با آن مواجه شدید).

    راه‌حل: خودمان، قبل از بازآرایی، پاراگراف را بر اساس تعداد کاراکتر
    به خط‌های کوتاه‌تر می‌شکنیم؛ سپس هر خطِ از قبل شکسته‌شده را rtl
    می‌کنیم. Label باید طوری تنظیم شود که دیگر خودش شکست خط اضافه نزند
    (یعنی اندازه‌ی افقی‌اش را به اندازه‌ی کافی بزرگ بگذاریم).
    """
    if not text:
        return text
    paragraphs = text.split("\n")
    out_lines = []
    for para in paragraphs:
        if not para.strip():
            out_lines.append("")
            continue
        words = para.split(" ")
        current = ""
        for word in words:
            candidate = (current + " " + word).strip()
            if len(candidate) > max_chars and current:
                out_lines.append(current)
                current = word
            else:
                current = candidate
        if current:
            out_lines.append(current)
    return rtl("\n".join(out_lines))
