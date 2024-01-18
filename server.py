from flask import Flask, render_template, request
from recommendations import get_recommendations
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/recommendations')
def get_my_recommendations():
    anime = request.args.get('anime')
    recommendations = get_recommendations(anime=anime)
    return render_template (
        'anime.html',
        Title=recommendations['AnimeList'][0]['Title'],
        Score=recommendations['AnimeList'][0]['Score'],
        Rank=recommendations['AnimeList'][0]['Rank'],
        Popularity=recommendations['AnimeList'][0]['Popularity'],
        MALPage=recommendations['AnimeList'][0]['MALPage'],
    )

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)