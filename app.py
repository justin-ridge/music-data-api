from flask import Flask, request
from flask_cors import CORS
import songs
import compress

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
compress.unzip_db()

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
    
if __name__ == '__main__':
    app.run(debug=True)