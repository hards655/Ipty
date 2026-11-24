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


def compare(serial):
    adb = [tool('adb', 'platform-tools')]
    if serial:
        adb += ['-s', serial]
    else:
        adb += ['-e']
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
    p.add_argument('action', choices=['setup', 'run', 'compare'])
    p.add_argument('--serial', help='ADB device serial for compare')
    args = p.parse_args()
    try:
        if args.action == 'setup':
            setup()
        elif args.action == 'run':
            run()
        else:
            compare(args.serial)
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode) from e


if __name__ == '__main__':
    main()
