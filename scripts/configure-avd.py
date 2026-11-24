from pathlib import Path
import os

home = Path(os.environ.get('ANDROID_AVD_HOME', Path.home() / '.android' / 'avd'))
config = home / 's23_api35.avd' / 'config.ini'
if not config.is_file():
    raise FileNotFoundError(config)
overlay = dict(line.split('=', 1) for line in Path('config.ini').read_text().splitlines() if line and not line.startswith('#'))
lines = [line for line in config.read_text().splitlines() if line.split('=', 1)[0] not in overlay]
lines.extend(f'{k}={v}' for k, v in overlay.items())
config.write_text('\n'.join(lines) + '\n')
