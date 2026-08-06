"""
farsi_widgets.py
-----------------
PersianTextInput: نسخه‌ای از TextInput که حین تایپ، حروف فارسی را
می‌چسباند (joining) و ترتیب راست‌به‌چپشان را درست نشان می‌دهد.

نکته‌ی مهم درباره‌ی طراحی: نسخه‌ی قبلی این فایل از یک ترفند «متن نامرئی
+ Label روکش» استفاده می‌کرد، ولی چون آن روش باعث می‌شد کلیک روی وسط
متن به موقعیت اشتباهی نگاشت شود (چون مختصات کلیک با متنِ واقعاً
نامرئی مطابقت نداشت)، ویرایش وسط جمله را خراب می‌کرد. برای همین به
نمایش مستقیمِ خودِ TextInput برگشتیم: همان چیزی که کاربر می‌بیند، همان
چیزی است که Kivy برای موقعیت مکان‌نما/کلیک استفاده می‌کند، پس ویرایش
همیشه در جای درست انجام می‌شود.

رفع باگِ «جابه‌جا شدن حروف»: نسخه‌ی قبلی این کلاس فقط reshape (چسباندن
حروف) را انجام می‌داد و ترتیب راست‌به‌چپ را به base_direction='rtl' در
theme.kv واگذار می‌کرد. مشکل این بود که هم reshape و هم مکانیزم داخلی
bidi خود Kivy، هر دو همزمان روی ترتیب/جهت متن اثر می‌گذاشتند و با هم
تداخل پیدا می‌کردند؛ نتیجه‌اش همین به‌هم‌ریختگی حروف بود (مثلاً «نازنین»
بهم ریخته نمایش داده می‌شد). راه‌حل: کل پردازش (چسباندن حروف + تعیین
ترتیب نمایش) را همین‌جا و یکجا با bidi.get_display انجام می‌دهیم و
دیگر به base_direction روی خودِ ویجت متکی نیستیم (در theme.kv هم حذف
شده) تا فقط یک مکانیزم روی متن اثر بگذارد.
"""

from kivy.uix.textinput import TextInput

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    _reshaper = arabic_reshaper.ArabicReshaper()
    _HAS_RESHAPER = True
except ImportError:
    _HAS_RESHAPER = False


class PersianTextInput(TextInput):
    def _create_line_label(self, text, hint=False):
        if _HAS_RESHAPER and text:
            try:
                text = get_display(_reshaper.reshape(text))
            except Exception:  # noqa: BLE001
                pass
        return super()._create_line_label(text, hint=hint)


# نگه‌داشتن نام قدیمی برای سازگاری با کدهایی که هنوز PersianInputBox
# را ایمپورت می‌کنند
PersianInputBox = PersianTextInput
