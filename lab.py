"""Create an official Android 15 AVD and compare its actual properties to a reference."""
import argparse
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

NAME = 'dm1q_api35_lab'
IMAGE = 'system-images;android-35;google_apis;x86_64'
ROOT = Path(__file__).resolve().parent


def tool(name, relative):
    sdk = os.environ.get('ANDROID_HOME') or os.environ.get('ANDROID_SDK_ROOT')
    if sdk:
        p = Path(sdk) / relative / name
        for candidate in (p, p.with_suffix('.exe'), p.with_suffix('.bat')):
            if candidate.is_file():
                return str(candidate)
    found = shutil.which(name)
    if found:
        return found
    raise SystemExit(f'Cannot find {name}. Install Android SDK and set ANDROID_HOME.')


def setup():
    if platform.machine().lower() not in ('x86_64', 'amd64'):
        raise SystemExit('This project uses an x86_64 emulator image; use an x86_64 host.')
    sdkmanager = tool('sdkmanager', 'cmdline-tools/latest/bin')
    avdmanager = tool('avdmanager', 'cmdline-tools/latest/bin')
    subprocess.run([sdkmanager, '--licenses'], check=True)
    subprocess.run([sdkmanager, 'platform-tools', 'emulator', IMAGE], check=True)
    emulator = tool('emulator', 'emulator')
    existing = subprocess.check_output([emulator, '-list-avds'], text=True).splitlines()
    if NAME not in existing:
        subprocess.run([avdmanager, 'create', 'avd', '-n', NAME, '-k', IMAGE],
                       input='no\n', text=True, check=True)
    else:
        print(f'AVD {NAME} already exists; left unchanged.')


def run():
    subprocess.run([tool('emulator', 'emulator'), '-avd', NAME], check=True)


def adb_command(serial):
    adb = [tool('adb', 'platform-tools')]
    return adb + (['-s', serial] if serial else ['-e'])


def configure(serial):
    """Set the active Android device name on the lab emulator and verify the OS."""
    adb = adb_command(serial)

    def shell(*args):
        return subprocess.check_output(adb + ['shell', *args], text=True).strip()

    if shell('getprop', 'ro.kernel.qemu') != '1' and shell('getprop', 'ro.boot.qemu') != '1':
        raise SystemExit('Only an Android emulator may be configured.')
    for key, expected in [('ro.build.version.release', '15'), ('ro.build.version.sdk', '35')]:
        actual = shell('getprop', key)
        if actual != expected:
            raise SystemExit(f'{key}: expected {expected}, got {actual}')
        print(f'{key}={actual}')
    name = 'SM-S911B-LAB'
    shell('settings', 'put', 'global', 'device_name', name)
    if shell('settings', 'get', 'global', 'device_name') != name:
        raise SystemExit('Device name verification failed.')
    print(f'Active Android device_name={name}')
    print('Hardware, build fingerprint and security properties remain genuine.')


def compare(serial):
    adb = adb_command(serial)
    output = subprocess.check_output(adb + ['shell', 'getprop'], text=True)
    actual = dict(re.findall(r'^\[([^\]]+)\]: \[(.*)\]$', output, re.M))
    expected = dict(line.split('=', 1) for line in (ROOT / 'profile.properties').read_text().splitlines()
                    if line and not line.startswith('#'))
    matches = 0
    for key, value in expected.items():
        observed = actual.get(key, '<absent>')
        equal = observed == value
        matches += equal
        print(f'{"OK" if equal else "DIFF"} {key}: actual={observed} | reference={value}')
    print(f'Matches: {matches}/{len(expected)}. No system properties changed.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('action', choices=['setup', 'run', 'configure', 'compare'])
    p.add_argument('--serial', help='ADB device serial for compare')
    args = p.parse_args()
    try:
        if args.action == 'setup':
            setup()
        elif args.action == 'run':
            run()
        elif args.action == 'configure':
            configure(args.serial)
        else:
            compare(args.serial)
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode) from e


if __name__ == '__main__':
    main()
