import os
from flask import Flask, render_template, request
import requests
from flask_caching import Cache

# Initialize Flask app
app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

# Proxy Config 🚀
PROXY_BASE_URL = "https://mitochondriaz36.replit.app/api/search"
TMDB_IMAGE_URL = "https://image.tmdb.org/t/p/w300"

# 🔍 Function to fetch movies via Proxy
@cache.cached(timeout=3600)
def get_movies(query="inception", page="1"):
    print(f"\n🔎 Calling get_movies() with query: '{query}'")
    params = {
        "q": query
    }

    try:
        response = requests.get(PROXY_BASE_URL, params=params, timeout=10)
        print(f"🌐 Proxy URL: {response.url}")
        print(f"📨 Raw proxy response text:\n{response.text[:500]}...")  # Preview first 500 chars
        data = response.json()

        movies = data.get("results", [])
        print(f"✅ Extracted {len(movies)} movies from proxy.")

        for movie in movies:
            movie["poster_url"] = TMDB_IMAGE_URL + movie["poster_path"] if movie.get("poster_path") else ""
        return movies
    except Exception as e:
        print("⚠️ Proxy error:", e)
        return []

# 🏠 Homepage route: genre-based sections
@app.route('/')
def index():
    print("\n🏠 Rendering homepage...")
    genres = ["Action", "Comedy", "Drama", "Horror", "Romance", "Thriller"]
    movies_by_genre = {}

    for genre in genres:
        movies = get_movies(query=genre)
        print(f"🎬 Genre '{genre}' → {len(movies)} movies")
        if movies:
            movies_by_genre[genre] = movies[:6]
    print("🧩 Final movies_by_genre keys:", list(movies_by_genre.keys()))
    return render_template('index.html', movies_by_genre=movies_by_genre)

# 🔎 Search route
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    print(f"\n🔍 Received search query: '{query}'")
    movies = get_movies(query=query) if query else []
    print(f"📊 Search returned {len(movies)} movies")
    return render_template('search.html', movies=movies, query=query)

# 🚀 Run the app
if __name__ == '__main__':
    print("🚀 Starting Movie Explorer app...")
    app.run(debug=True, port=1912)