from pathlib import Path
from datetime import datetime
import random

def valid_date(year, month, day, hour=0, minute=0, second=0):
    try:
        datetime(year, month, day, hour, minute, second)
        return True
    
    except ValueError: 
        return False    

root = Path('test')
des = root / 'source'
des.mkdir(parents=True, exist_ok=True)

count = 0

while count < 300:
    year = random.randint(2015, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 31)

    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    if valid_date(year, month, day, hour, minute, second):
        
        file_name = f'{year}{month:02d}{day:02d}_{hour:02d}{minute:02d}{second:02d}.txt'
        (des / file_name).touch()
        count += 1