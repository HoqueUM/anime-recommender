from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import csv
import requests
from fake_useragent import UserAgent
import time
import random
import pandas as pd

df = pd.read_csv('valid_pages.csv')

ua = UserAgent()
pages = df['Page'].tolist()
sleep_intervals = [1, 2, 3]
with open('valid_pages.csv', 'a', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(['Page'])

    for page in pages:
            disable_warnings(InsecureRequestWarning)
            headers = {'User-Agent': str(ua.random)}
            url = f'https://myanimelist.net/anime/{page}'
            status = requests.get(url, headers=headers, verify=False).status_code
            print(f'Status: {status}')

            if 200 <= status <= 300:
                  print(f'Page #{page} is valid.')
                  writer.writerow([page])
            else:
                  print(f'Page #{page} is invalid.')
                  
            page += 1
            sleep_time = sleep_intervals[random.randint(0, len(sleep_intervals) - 1)]
            print(f'Sleep time: {sleep_time}')
            time.sleep(sleep_time)
            print('Resumed\n')