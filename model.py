# the carry: https://medium.com/@prateekgaurav/step-by-step-content-based-recommendation-system-823bbfd0541c#:~:text=Content%2Dbased%20recommendation%20systems%20are,their%20viewing%20and%20purchasing%20history.

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('C:\\Users\\rahul\\projects\\My Anime List Dataset 2024.csv')

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

model_pkl_file = 'anime_recommendation.pkl'

with open(model_pkl_file, 'wb') as file:
    pickle.dump(similarity_df, file)

# Ask the user for a movie they like
movie = input('Enter a movie you like: ')

# Find the index of the movie in the similarity dataframe
movie_index = similarity_df.index.get_loc(movie)

# Get the top 5 most similar movies to the movie
top_10 = similarity_df.iloc[movie_index].sort_values(ascending=False)[1:11]

# Print the top 5 most similar movies to the movie
print(f'Top 10 similar movies to {movie}:')
print(top_10)
