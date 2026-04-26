[app]
title           = Aurelius Academy
package.name    = aureliusacademy
package.domain  = org.aurelius

source.dir      = .
source.include_exts = py,png,jpg,kv,atlas,json,db

version         = 2.0

requirements    = python3,kivy==2.3.0,kivymd,anthropic,pypdf,sqlite3,certifi,charset-normalizer,urllib3,requests,openssl

orientation     = portrait
fullscreen      = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api         = 33
android.minapi      = 26
android.ndk         = 25b
android.ndk_api     = 21
android.arch        = arm64-v8a

android.enable_androidx    = True
android.gradle_dependencies = 'androidx.core:core:1.10.1'

# Icon & splash (place 512x512 PNG in assets/)
icon.filename    = %(source.dir)s/assets/icon.png
presplash.filename = %(source.dir)s/assets/splash.png
presplash.color  = #0d0d1a

[buildozer]
log_level = 2
warn_on_root = 1
