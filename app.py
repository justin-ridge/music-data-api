import flask as fl
from flask import abort, escape
from flask_cors import CORS
import http
import songs
import compress
import probability
import pickle
import datamanipulation

app = fl.Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
compress.unzip_db()
model = pickle.load(open('naive_bayes.sav', 'rb'))

@app.route('/api/songs/<songid>', methods=['GET'])
def get_song(songid):
    return songs.get_song(songid)

@app.route('/api/songs', methods=['GET'])
def get_songs():
    page = escape(fl.request.args.get('page'))
    metadata = escape(fl.request.args.get('metadata'))

    if page is None or not page.isnumeric():
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
    name = escape(fl.request.args.get('name'))
    artist = escape(fl.request.args.get('artist'))
    genre = escape(fl.request.args.get('genre'))

    if name is None:
        name = ''

    if artist is None:
        artist = ''

    if genre is None:
        genre = ''

    return songs.search(name, artist, genre)

@app.route('/api/songs/predict', methods=['POST'])
def predict():
    data = fl.request.json
    result = probability.predict(model, data)
    return fl.jsonify(result)

@app.route('/api/songs/prepdata', methods=['POST'])
def prep_data():
    try:
        posted_file = fl.request.json['data']
        zipped_file = datamanipulation.prep_data(posted_file)
        return fl.send_file(zipped_file, attachment_filename='clean_data.zip', as_attachment=True)
    except:
        abort(400)

@app.route('/api/songs/naivebayes', methods=['POST'])
def naive_bayes():
    try:
        posted_file = fl.request.json['data']
        result = datamanipulation.naive_bayes(posted_file)
        return fl.jsonify(result)
    except:
        abort(400)

@app.route('/api/songs/randomforest', methods=['POST'])
def random_forest():
    try:
        posted_file = fl.request.json['data']
        result = datamanipulation.random_forest(posted_file)
        return fl.jsonify(result)
    except:
        abort(400)

@app.errorhandler(500)
def internal_error(error):
    return "An unknown error has occurred."

@app.errorhandler(400)
def bad_request(error):
    return "Bad request: please verify that your data is formatted correctly and try again.", 400

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response
    
if __name__ == '__main__':
    app.run(debug=True)