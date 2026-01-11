from pathlib import Path
import re
import shutil

root = Path('test')
source = root / 'source'
destination = root / 'destination'

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