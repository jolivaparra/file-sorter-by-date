import logging
import re
import shutil
from pathlib import Path

from tqdm import tqdm


def load_config(config_file: Path) -> tuple[Path, Path] | None:
    """Extracts source and destination paths from the configuration file.

    Args:
        config_file (Path): Path object pointing to the configuration file.

    Returns:
        tuple[Path, Path] | None: A tuple containing (source, destination) if both paths
                                  are found in the file.
                                  Returns None if the config file is missing or the paths
                                  are not defined correctly.
    """

    if config_file.exists():
        with open(config_file, "r") as configs:
            content = configs.read()
            src = re.search(r'Source: "(.*)"', content)
            dst = re.search(r'Destination: "(.*)"', content)

            if src and dst:
                source = Path(src.group(1))
                destination = Path(dst.group(1))
                return (source, destination)
            else:
                print("Source path not found, or paths missing.")
                input()
                return None
    else:
        print("'config.txt' file not found.")
        input()
        return None


def scan_files(source: Path) -> tuple[dict, int]:
    """Scans the source directory for files matching the date pattern YYYYMMDD.

    Args:
        source (Path): The directory path to scan for files.

    Returns:
        tuple[dict, int]: A tuple containing:
            - A dictionary mapping date tuples (year, month, day) to lists of filenames.
            - An integer representing the total number of valid files found.
    """

    # Regex to capture Year(1), Month(2), and Day(3) from filenames like '20240125_...'
    regex = re.compile(r"(20\d{2})(\d{2})(\d{2})_\d+")

    files = source.glob("*.*")
    days = {}
    total_files = 0

    for file in files:
        info = regex.search(file.stem)
        if info:
            if info.groups() not in days:
                days[info.groups()] = []

            days[info.groups()].append(file.name)
            total_files += 1

    return (days, total_files)


def should_skip_file(src: Path, dst: Path, file: str) -> bool:
    """Checks if a file in the source folder already exists in the destination folder.

    Args:
        src (Path): Path object pointing to the source folder.
        dst (Path): Path object pointing to the destination folder.
        file (str): Name of the file to check.

    Returns:
        bool: True if the file exists in destination and has the same size (duplicate),
              False otherwise.
    """

    if (dst / file).exists():
        if (src / file).stat().st_size == (dst / file).stat().st_size:
            return True
    return False


def main(CONFIG_FILE):
    """Orchestrates the file sorting process based on the provided configuration.

    Flow:
        1. Sets up logging.
        2. Loads configuration (source/destination).
        3. Scans for files.
        4. Moves files into date-based folders with a progress bar.

    Args:
        CONFIG_FILE (Path): Path to the configuration file (e.g., config.txt).
    """

    logging.basicConfig(
        filename="file-sorter-register.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding="utf-8",
    )

    config_data = load_config(CONFIG_FILE)

    if config_data is None:
        return

    source_folder, destination_folder = config_data
    days, total_files = scan_files(source_folder)

    logging.info(f"--- Starting process ---")
    logging.info(f"Source: {source_folder}")
    logging.info(f"Destination: {destination_folder}")

    with tqdm(total=total_files, unit="file", ncols=100) as pbar:
        for date in days:
            year, month, day = date

            # If a day has few photos (<=4), group them into a monthly "Varied" folder
            # to avoid creating too many small folders.
            if len(days[date]) > 4:
                file_dst_folder = destination_folder / year / f"{year}-{month}-{day}"
            else:
                file_dst_folder = destination_folder / year / f"{year}-{month} Varied"

            file_dst_folder.mkdir(parents=True, exist_ok=True)

            for file in days[date]:
                file_size = (source_folder / file).stat().st_size / 1024**2
                pbar.set_postfix(file=file[:20], MB=f"{file_size:.2f}")

                if should_skip_file(source_folder, file_dst_folder, file):
                    pbar.update(1)
                    logging.warning(f"Skipping duplicate: '{file}'")
                    continue

                try:
                    shutil.move(source_folder / file, file_dst_folder / file)
                    logging.info(f"Successful transfer '{file}' -> '{file_dst_folder}'")
                except Exception as e:
                    # Log error to continue processing the rest of the queue
                    logging.error(f"Error processing '{file}': {e}")
                    tqdm.write(f"Error in '{file}': {e}")

                pbar.update(1)

    logging.info(f"Process finished. Total files processed: {total_files}")


if __name__ == "__main__":
    main(Path("config.txt"))
