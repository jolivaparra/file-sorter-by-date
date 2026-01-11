# Samsung Image File Sorter

This repository contains a script to sort Samsung image files that use the naming convention `{year}{month}{day}-{hour}{minute}{second}.jpg`.

## Sorting Logic:
1. Every image is sorted by year into a directory `{year}/` in the destination path.
2. If there are **more than 4 images taken** on the same day, the files will be saved in a specific day directory: `{year}/{year}-{month}-{day}/`.
3. If there are **4 or fewer images taken** on the same day, the files will go to a general directory: `{year}/{year}-{month} Varied/`.