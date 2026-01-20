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
            print('Rutas de origen y destino no encontradas.')
            input()
            exit()
else:
    print('Archivo de configuraciones no encontrado.')
    input()
    exit()

regex = re.compile(r'(20\d{2})(\d{2})(\d{2})_\d+')

files = source.glob('*.*')
days = {}

for file in files:
    info = regex.search(file.stem)
    if info:
        if info.groups() not in days:
            days[info.groups()] = []

        days[info.groups()].append(file.name)

for date in days:
    year, month, day = date

    if len(days[date])>4:
        dst = destination / year / f'{year}-{month}-{day}'
    else:
        dst = destination / year / f'{year}-{month} Variados'
    
    dst.mkdir(parents=True, exist_ok=True)

    for file in days[date]:
        shutil.move(source / file, dst / file)            