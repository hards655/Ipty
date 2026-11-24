#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
adb shell getprop > artifacts/getprop.txt
adb shell wm size > artifacts/display.txt
adb shell wm density >> artifacts/display.txt
adb shell getprop ro.build.version.sdk | tr -d '\r' | grep -qx 35
adb shell getprop sys.boot_completed | tr -d '\r' | grep -qx 1
adb shell input keyevent KEYCODE_WAKEUP
adb shell input keyevent KEYCODE_HOME
adb exec-out screencap -p > artifacts/screenshot.png
