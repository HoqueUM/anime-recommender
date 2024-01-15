import pickle
import pandas as pd
import json

def get_recommendations(anime, score=7.0, rank=1000, num_shows=10):
    with open('anime_recommendation.pkl', 'rb') as file:
        model = pickle.load(file)
    
    try:
        anime_index = model.index.get_loc(anime)
    except KeyError:
        print(f'{anime} is not listed in database. Please try again.')
        return
    
    closest = model.iloc[anime_index].sort_values(ascending=False)

    df = pd.DataFrame(closest)

    titles_list = df[anime].index.tolist()

    full_list = []
    substrings = ['Dragon Ball', 'Naruto', 'Naruto Shippuden', 'Boruto', 'Boruto: Naruto Next Generations', 'Shadow Skill', 'Fairy Tail', 'One Piece', 'Swallowed Star', 'The Seven Deadly Sins', 'Overlord ', 'Major S', 'Chihayafuru', 'Ranma ½', 'City Hunter', 'Broken Blade', 'Buddy Go!', 'Blame!', 'Eat-Man', 'OVA', 'Movie', '2', '3', '4', '5', 'K-On!', 'Slayers']


    def substring_checker(string):
        for i in range(len(substrings)):
            if string == anime:
                return False
            elif string == substrings[i]:
                return True
            elif substrings[i] in string:
                return False
        return True
    
    for i in range(len(titles_list)):
        if substring_checker(titles_list[i]) and len(titles_list[i]) <= 15 and titles_list[i] not in full_list:
            full_list.append(titles_list[i]) 

    #convert into database
    anime_df = pd.read_csv('My Anime List Dataset 2024.csv')
    scores = anime_df['Score'].tolist()
    ranks = anime_df['Rank'].tolist()
    popularity = anime_df['Popularity'].tolist()
    img = anime_df['Image Link'].tolist()
    mal = anime_df['MAL Page'].tolist()
    titles = anime_df['English'].tolist()

    refined_list = []

    for i in range(0, len(full_list)//4):
        ind = titles.index(full_list[i])
        if score == 0 and rank != 0:
            if ranks[ind] <= rank:
                refined_list.append(full_list[i])
        elif rank==0 and score != 0:
            if scores[ind] >= score:
                refined_list.append(full_list[i])
        elif score==0 and rank==0:
            refined_list.append(full_list[i])
    
        elif scores[ind] >= score and ranks[ind] <= rank:
            refined_list.append(full_list[i])

    anime_data = {
        "AnimeList" : [
        ]
    }
    if len(refined_list) < num_shows:
        for i in range(0, len(refined_list)):
            ind = titles.index(refined_list[i])
            anime_data['AnimeList'].append({
                "Title": titles[ind],
                "Score": scores[ind],
                "Rank": ranks[ind],
                "Popularity": popularity[ind],
                "ImageLink": img[ind],
                "MALPage": mal[ind]
            })
    else:
        for i in range(0, num_shows):
            ind = titles.index(refined_list[i])
            anime_data['AnimeList'].append({
                "Title": titles[ind],
                "Score": scores[ind],
                "Rank": ranks[ind],
                "Popularity": popularity[ind],
                "ImageLink": img[ind],
                "MALPage": mal[ind]
            })

    # Save as JSON file
    with open('anime_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(anime_data, json_file, ensure_ascii=False, indent=4)
    
    if num_shows >= len(refined_list):
        return refined_list, full_list
    return refined_list[0:num_shows], full_list




my_recs, valid_titles = get_recommendations('Goblin Slayer', rank=2500,num_shows=20)
print(my_recs)



