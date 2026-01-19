from pathlib import Path
import re
import shutil

config_file = Path('config.txt')

if config_file.exists():
    with open(config_file, 'r') as configs:
        content = configs.read()
        src = re.search(r'Source: "(.*)"', content)
        dst = re.search(r'Destination: "(.*)"', content)

        if src and dst:
            source = Path(src.group(1))
            destination = Path(dst.group(1))
else:
    print('Archivo de configuraciones no encontrado.')
    input()

regex = re.compile(r'(20\d{2})(\d{2})(\d{2})_\d+')

files = source.glob('*.*')
days = []

for file in files:
    info = regex.search(file.stem)
    if info:
        days.append(info.groups())

files = source.glob('*.*')

for file in files:
    info = regex.search(file.stem)
    if info:
        year, month, day = info.groups()

        if days.count(info.groups())>4:
            des = destination / year / f'{year}-{month}-{day}'
            des.mkdir(parents=True, exist_ok=True)
            shutil.move(file, des / file.name)
        else:
            des = destination / year / f'{year}-{month} Variados'
            des.mkdir(parents=True, exist_ok=True)
            shutil.move(file, des / file.name)