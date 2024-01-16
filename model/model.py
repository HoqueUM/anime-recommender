# the carry: https://medium.com/@prateekgaurav/step-by-step-content-based-recommendation-system-823bbfd0541c#:~:text=Content%2Dbased%20recommendation%20systems%20are,their%20viewing%20and%20purchasing%20history.
# helpful link: https://stackoverflow.com/questions/57983431/whats-the-most-space-efficient-way-to-compress-serialized-python-data

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import warnings
import bz2
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('My Anime List Dataset 2024.csv')

df = df.dropna(subset=['Genres', 'Score', 'Rank', 'Popularity', 'Number of Scores'])

genres = df['Genres'].str.split(",").tolist()
scores = df['Score'].tolist()
ranks = df['Rank'].tolist()
popularity = df['Popularity'].tolist()
number_of_scores = df['Number of Scores'].tolist()
titles = df['English']


# create bag of words representation of genres

for ls in range(len(genres)):
    genres[ls].append(str(scores[ls]))
    genres[ls].append(str(ranks[ls]))
    genres[ls].append(str(popularity[ls]))
    genres[ls].append(str(number_of_scores[ls]))

def create_bow(genre_list):
    bow = {}
    for genre in genre_list:
        bow[genre] = 1
    
    return bow

# Create a list of bags of words representations of the movie genres
bags_of_words = [create_bow(anime_genres)for anime_genres in genres]
 
# Create a dataframe to store the bags of words representation of the movie genres
genre_df = pd.DataFrame(bags_of_words, index=titles).fillna(0)

# Calculate the cosine similarity matrix between the movies
cosine_similarity = cosine_similarity(genre_df)

# Create a dataframe with the cosine similarity scores
similarity_df = pd.DataFrame(cosine_similarity, index=genre_df.index, columns=genre_df.index)


with bz2.BZ2File('anime_recommendation.pbz2', 'wb') as file:
    pickle.dump(similarity_df, file)




