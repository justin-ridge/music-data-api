from flask import Flask, request, jsonify
from flask_cors import CORS
import songs
import compress
import probability
import pickle

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
compress.unzip_db()
model = pickle.load(open('naive_bayes.sav', 'rb'))

@app.route('/api/songs/<songid>', methods=['GET'])
def get_song(songid):
    return songs.get_song(songid)

@app.route('/api/songs', methods=['GET'])
def get_songs():
    page = request.args.get('page')
    metadata = request.args.get('metadata')

    if page is None:
        page = '0'

    if metadata == 'features':
        return songs.get_songs_features(page)
    elif metadata == 'minmax':
        return songs.get_songs_minmax(page)
    else:
        return songs.get_songs(page)

@app.route('/api/songs/pagecount', methods=['GET'])
def get_page_count():
    return songs.get_page_count()

@app.route('/api/songs/count', methods=['GET'])
def get_count():
    return songs.get_count()

@app.route('/api/songs/search', methods=['GET'])
def search_songs():
    name = request.args.get('name')
    artist = request.args.get('artist')
    genre = request.args.get('genre')

    if name is None:
        name = ''

    if artist is None:
        artist = ''

    if genre is None:
        genre = ''

    return songs.search(name, artist, genre)

@app.route('/api/songs/predict', methods=['POST'])
def predict():
    data = request.json
    result = probability.predict(model, data)
    return jsonify(result)
    
if __name__ == '__main__':
    app.run(debug=True)