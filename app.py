import flask as fl
from flask_cors import CORS
import http
import songs
import compress
import probability
import pickle
import prepdata

app = fl.Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
compress.unzip_db()
model = pickle.load(open('naive_bayes.sav', 'rb'))

@app.route('/api/songs/<songid>', methods=['GET'])
def get_song(songid):
    return songs.get_song(songid)

@app.route('/api/songs', methods=['GET'])
def get_songs():
    page = fl.request.args.get('page')
    metadata = fl.request.args.get('metadata')

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
    name = fl.request.args.get('name')
    artist = fl.request.args.get('artist')
    genre = fl.request.args.get('genre')

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
    posted_file = fl.request.json['data']
    zipped_file = prepdata.prep_data(posted_file)
    return fl.send_file(zipped_file, attachment_filename='clean_data.zip', as_attachment=True)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response
    
if __name__ == '__main__':
    app.run(debug=True)

#2.71.10 or 11, also check 2.83, no config
#3421
#3415
#check 3425 tshirt