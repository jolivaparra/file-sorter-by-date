from pathlib import Path
import re
import shutil
from tqdm import tqdm
import time

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
total_files = 0

for file in files:
    info = regex.search(file.stem)
    if info:
        if info.groups() not in days:
            days[info.groups()] = []

        days[info.groups()].append(file.name)
        total_files+=1

with tqdm(total=total_files, unit='file', ncols=100) as pbar:
    for date in days:
        year, month, day = date

        if len(days[date])>4:
            dst = destination / year / f'{year}-{month}-{day}'
        else:
            dst = destination / year / f'{year}-{month} Variados'
        
        dst.mkdir(parents=True, exist_ok=True)

        for file in days[date]:
            file_size = (source/file).stat().st_size / 1024**2
            pbar.set_postfix(file=file[:20],mb=f'{file_size:.2f}')

            if (dst / file).exists():
                if (source / file).stat().st_size==(dst / file).stat().st_size:
                    pbar.update(1)
                    continue

            shutil.copy2(source / file, dst / file)
            pbar.update(1)