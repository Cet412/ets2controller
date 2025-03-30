[app]

# Basic App Info
title = ETS2 Controller
package.name = ets2controller
package.domain = org.kivy
version = 0.1

# Files and Sources
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav
orientation = landscape
fullscreen = 1
icon.filename = icon.png

# Requirements (Optimized for Bluetooth)
requirements = 
    python3,
    kivy==2.1.0,
    pyjnius,
    android,
    plyer,
    pybluez-android

# Android Config
android.api = 31
android.minapi = 21
android.sdk_version = 31
android.ndk_version = 25b
android.archs = arm64-v8a,armeabi-v7a
android.skip_openssl = True

# Permissions (Bluetooth)
android.permissions = 
    INTERNET,
    BLUETOOTH,
    BLUETOOTH_ADMIN,
    BLUETOOTH_CONNECT,
    BLUETOOTH_SCAN,  # Diperlukan untuk Android 12+
    ACCESS_COARSE_LOCATION,
    ACCESS_FINE_LOCATION

# Build Optimization
android.num_cores = 4  # Use 4 CPU cores
android.wakelock = True
android.allow_backup = False
android.debuggable = True

# Advanced
p4a.extra_args = --ignore-setup-py --no-deps
android.ndk_args = -Wno-macro-redefined

[buildozer]
log_level = 2
warn_on_root = 1