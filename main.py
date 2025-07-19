from flask import Flask, request, jsonify
import requests
import os

app = Flask(_name_)

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    api_key = os.environ.get("TMDB_API_KEY")
    if not api_key:
        return jsonify({"error": "Missing TMDB API key"})

    res = requests.get("https://api.themoviedb.org/3/search/movie", params={"api_key": api_key, "query": query})
    return jsonify(res.json())

@app.route('/')
def home():
    return "✅ TMDB Proxy is Running"

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))