[app]

title = Dream Dictionary
package.name = dreamdictionary
package.domain = org.dreamdictionary

source.dir = .
source.include_exts = py,json,png,jpg,kv

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 35
android.minapi = 23

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
