from pathlib import Path
import re
import shutil
from tqdm import tqdm
import logging

def load_config(config_file: Path) -> tuple[Path, Path] | None:
    if config_file.exists():
        with open(config_file, 'r') as configs:
            content = configs.read()
            src = re.search(r'Source: "(.*)"', content)
            dst = re.search(r'Destination: "(.*)"', content)

            if src and dst:
                source = Path(src.group(1))
                destination = Path(dst.group(1))
                return (source, destination)
            else:
                print('Rutas de origen y destino no encontradas.')
                input()
                return None
    else:
        print('Archivo de configuraciones no encontrado.')
        input()
        return None

def scan_files(source: Path) -> tuple[dict, int]:
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

    return (days, total_files)

def should_skip_file(src: Path, dst: Path, file: str) -> bool:
    if (dst / file).exists():
        if (src / file).stat().st_size==(dst / file).stat().st_size:
            return True
    return False

def main(CONFIG_FILE):

    logging.basicConfig(
        filename='file-sorter-register.log',
        filemode='w',                       
        level=logging.INFO,                  
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8'
    )

    config_data = load_config(CONFIG_FILE)

    if config_data is None:
        return

    source_folder, destination_folder = config_data
    days, total_files = scan_files(source_folder)

    logging.info(f"--- Inicio del proceso ---")
    logging.info(f"Origen: {source_folder}")
    logging.info(f"Destino: {destination_folder}")

    with tqdm(total=total_files, unit='file', ncols=100) as pbar:
        for date in days:
            year, month, day = date

            if len(days[date])>4:
                file_dst_folder = destination_folder / year / f'{year}-{month}-{day}'
            else:
                file_dst_folder = destination_folder / year / f'{year}-{month} Variados'
            
            file_dst_folder.mkdir(parents=True, exist_ok=True)


            for file in days[date]:
                file_size = (source_folder/file).stat().st_size / 1024**2
                pbar.set_postfix(file=file[:20],MB=f'{file_size:.2f}')

                if should_skip_file(source_folder, file_dst_folder, file):
                        pbar.update(1)
                        logging.warning(f"Saltado por duplicado: '{file}'")
                        continue

                try:
                    shutil.copy2(source_folder / file, file_dst_folder / file)
                    logging.info(f"Copiado exitoso '{file}' -> '{file_dst_folder}'")
                except Exception as e:
                    logging.error(f"Error procesando '{file}': {e}")                 
                    tqdm.write(f"Error en '{file}': {e}")
                pbar.update(1)
    
    logging.info(f'Proceso finalizado. Archivos procesados: {total_files}')


if __name__=='__main__':
    main(Path('config.txt'))