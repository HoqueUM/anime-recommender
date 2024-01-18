from bs4 import BeautifulSoup
import requests
import pandas as pd
from fake_useragent import UserAgent
import csv
import time
import random
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
disable_warnings(InsecureRequestWarning)

df = pd.read_csv('valid_pages.csv')

pages = df['Page'].tolist()

def scrape_mal (page, ua):
    url = f'https://myanimelist.net/anime/{page}'
    headers = {'User-Agent': ua}
    html = requests.get(url, headers=headers, verify=False)

    if html.status_code == 404:
        return None
    
    soup = BeautifulSoup(html.content, 'html.parser')

    transliterated = soup.find('h1', class_='title-name h1_bold_none').text
    english = soup.find('p', class_='title-english title-inherit').text if soup.find('p', class_='title-english title-inherit') else transliterated
    img = soup.find('img', itemprop='image').get('data-src') if soup.find('img', itemprop='image') else ''

    score_list = ['na', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
    for i in range(len(score_list)):
        if soup.find('div', class_=f'score-label score-{score_list[i]}'):
            score = soup.find('div', class_=f'score-label score-{score_list[i]}').text

    rank = soup.find('span', class_='numbers ranked').text.split(' ')[1].strip('#')

    overall_container = soup.find_all('div', class_='spaceit_pad')
    overall_intermediate = [item.text.strip().replace('\n', '') for item in overall_container]
    overall = [item.split(':') for item in overall_intermediate]
    final = [overall[i] for i in range(len(overall)) if len(overall[i]) == 2]

    genres_container = soup.find_all('span', itemprop='genre') if soup.find('span', itemprop='genre') else ''
    please = [item.text for item in genres_container]


    intermediate_dict = dict(final)
    anime_dict = {key: value.strip() for key, value in intermediate_dict.items()}

    anime_dict['Genres'] = ', '.join(map(str, please))

    webpage = soup.find('a', class_='link ga-click').get('href') if soup.find('a', class_='link ga-click') else ''

    scored_by = soup.find('span', itemprop='ratingCount').text if soup.find('span', itemprop='ratingCount') else ''

    anime_dict['Website'] = webpage

    anime_dict['Scored By #'] = scored_by

    japanese = anime_dict['Japanese'] if 'Japanese' in anime_dict else ''
    popularity = anime_dict['Popularity'].strip('#')
    type = anime_dict['Type'] if 'Type' in anime_dict else ''
    members = anime_dict['Members'] if 'Members' in anime_dict else ''
    favorites = anime_dict['Favorites'] if 'Favorites' in anime_dict else ''
    genres = anime_dict['Genres'] 
    studios = ' '.join(anime_dict['Studios'].split()) if 'Studios' in anime_dict else ''
    producers = ' '.join(anime_dict['Producers'].split()) if 'Producers' in anime_dict else ''
    licensors = ' '.join(anime_dict['Licensors'].split()) if 'Licensors' in anime_dict else ''
    episodes = anime_dict['Episodes'] if 'Episodes' in anime_dict else ''
    rating = anime_dict['Rating'][0:2] if 'Rating' in anime_dict else ''
    premiered = anime_dict['Premiered'] if 'Premiered' in anime_dict else ''
    aired = anime_dict['Aired'] if 'Aired' in anime_dict else ''
    website = anime_dict['Website'] if 'Website' in anime_dict else ''
    scored_by_number = anime_dict['Scored By #'] if 'Scored By #' in anime_dict else ''

    return (english, japanese, transliterated, img, type, episodes, rating, 
            genres, studios, producers, premiered, aired, score, scored_by_number,
            rank, popularity, members, favorites, website, page, url)

sleep_intervals = [1, 2, 3]
with open('My Anime List Dataset 2024.csv', 'a', newline='', encoding="utf-8") as file: # change to append when stopping
    writer = csv.writer(file)
    if file.tell() == 0:
        writer.writerow(['English', 'Japanese', 'Transliterated', 'Image Link', 'Type', 'Episodes',
                         'Rating', 'Genres', 'Studios', 'Producers', 'Premiered', 'Aired', 'Score', 'Number of Scores',
                         'Rank', 'Popularity', 'Members', 'Favorites', 'Anime Website', 'Page Number', 'MAL Link'])
        for page in pages:
            ua = str(UserAgent().random)
            response = scrape_mal(page, ua)
            if response is not None:
                (english, japanese, transliterated, img, type, episodes, rating,
                genres, studios, producers, premiered, aired, score, scored_by_number,
                rank, popularity, members, favorites, website, page_number, url) = response
                writer.writerow(
                    [english, japanese, transliterated, img, type, episodes, rating,
                    genres, studios, producers, premiered, aired, score, scored_by_number,
                    rank, popularity, members, favorites, website, page_number, url]
                )
            print(f'Page {pages.index(page) + 1}/{len(pages)} done. {(pages.index(page) + 1)/len(pages):.2f}% complete.')
            sleep_time = sleep_intervals[random.randint(0, len(sleep_intervals) - 1)]
            print(f'Sleep time: {sleep_time}')
            time.sleep(sleep_time)
            print('Resumed\n')
        