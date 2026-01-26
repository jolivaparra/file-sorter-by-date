# Date-Based File Sorter (v1.0)

A Python utility that organizes chaotic photo and video folders. It scans files for dates (YYYYMMDD_hhmmss format), sorts them into a structured directory hierarchy, and handles duplicates.

## Features

- **Smart Sorting:** Moves files into `Year / YYYY-MM-DD` folders.
- **"Varied" Logic:** Automatically groups days with few photos (≤4) into a monthly "Varied" folder to keep directories clean.
- **Duplicate Protection:** Checks destination for existing files with the same name and size to prevent overwriting or duplication.
- **Audit Logging:** Generates a detailed `file-sorter-register.log` tracking every move, skip, or error.

## Installation

1. **Clone the repository** (or download the script).
2. **Install dependencies:**
   Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Set the file `config.txt`. Use the following format:

```text
Source: "C:\Users\YourName\Downloads\UnsortedPhotos"
Destination: "C:\Backups\PhotoLibrary"
```

* **Note:** The script will MOVE files from Source to Destination. Ensure you have a backup of your source files before running it for the first time.

## Usage

Simply run the script with Python:

```bash
python file_sorter.py
```

## Safety Mechanisms

* **Activity Log:** Every action is recorded in file-sorter-register.log for full traceability.
* **Skip Logic:** If a file already exists in the destination and is identical (same size), the script skips it to save time and data integrity.
* **Error Handling:** If a specific file fails to move (e.g., permission error), the script logs the error and continues with the next file.

## Testing

The repository includes a utility to generate dummy data for testing purposes, allowing you to verify the script safely.

1.  **Generate Test Files:**
    Run the generator script to create 300 empty text files with random dates in `test/source`:
    ```bash
    python utils/test_generator.py
    ```

2.  **Run Sorter on Test Data:**
    The `config.txt` is already pointing to the test environment:
    ```text
    Source: "test/source"
    Destination: "test/destination"
    ```
    Then run the main script normally.