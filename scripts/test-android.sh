#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results
serial=127.0.0.1:5555
a() { adb -s "$serial" "$@"; }
adb start-server
for i in $(seq 1 120); do
  adb connect "$serial" >/dev/null 2>&1 || true
  if [[ $(a shell getprop sys.boot_completed 2>/dev/null | tr -d '\r' || true) == 1 ]]; then
    break
  fi
  sleep 5
done
test "$(a shell getprop sys.boot_completed | tr -d '\r')" = 1
test "$(a shell getprop ro.build.version.sdk | tr -d '\r')" = 35
a shell getprop > results/actual-properties.txt
a shell settings put global device_name SM-S911B-LAB
a shell input keyevent KEYCODE_WAKEUP
a shell wm dismiss-keyguard || true
a shell input keyevent KEYCODE_HOME
sleep 3
a exec-out screencap -p > results/android-home.png
test -s results/android-home.png
if [[ -f app/app.apk ]]; then
  a shell pm list packages -3 | tr -d '\r' | sort > results/packages-before.txt
  a install -r app/app.apk | tee results/install.txt
  a shell pm list packages -3 | tr -d '\r' | sort > results/packages-after.txt
  package="$(comm -13 results/packages-before.txt results/packages-after.txt | sed -n 's/^package://p')"
  if [[ -f app/package.txt ]]; then
    package="$(tr -d '\r\n' < app/package.txt)"
  fi
  if [[ ! "$package" =~ ^[a-zA-Z0-9_]+(\.[a-zA-Z0-9_]+)+$ ]]; then
    echo 'Cannot uniquely identify package. Set app/package.txt.' >&2
    exit 1
  fi
  activity="$(a shell cmd package resolve-activity --brief -a android.intent.action.MAIN -c android.intent.category.LAUNCHER "$package" | tr -d '\r' | tail -n 1)"
  if [[ "$activity" != "$package/"* ]]; then
    echo "No launcher activity for $package" >&2
    exit 1
  fi
  a shell am start -W -n "$activity" | tee results/launch.txt
  sleep 8
  a exec-out screencap -p > results/app-launch.png
  test -s results/app-launch.png
  a shell dumpsys activity activities > results/activities.txt
else
  echo 'No app/app.apk was provided; only Android home was captured.' | tee results/app-status.txt
fi
