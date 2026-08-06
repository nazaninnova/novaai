[app]
title = Nova AI
package.name = novaai
package.domain = org.yourname
source.dir = .
source.include_exts = py,kv,png,jpg,gguf
version = 1.0
requirements = python3,kivy,requests,pyjnius,plyer
# توجه مهم: llama-cpp-python اینجا نیست چون هیچ recipe رسمی برای
# python-for-android ندارد. راه‌حل: یک باینری llama-server از پیش
# کامپایل‌شده با NDK را به‌عنوان کتابخانه‌ی نیتیو اضافه می‌کنیم (پایین)
# و پایتون فقط با HTTP محلی به آن وصل می‌شود. جزئیات کامل در README.md.

orientation = portrait
fullscreen = 0

android.permissions = INTERNET, CAMERA, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES
android.api = 34
android.minapi = 24
android.ndk = 27d
android.archs = arm64-v8a
android.allow_backup = True

# باینری llama-server کراس‌کامپایل‌شده با NDK را اینجا اضافه می‌کنیم.
# اندروید فایل‌های داخل nativeLibraryDir را خودکار قابل‌اجرا می‌کند.
# ابتدا طبق README باینری‌ها را بسازید و به این مسیرها کپی کنید:
#   libs/arm64-v8a/libllama_server.so
#   libs/armeabi-v7a/libllama_server.so
android.add_libs_arm64_v8a = libs/arm64-v8a/libllama_server.so

[buildozer]
log_level = 2
warn_on_root = 1
