from flask import Flask
from flask import request
import songs

app = Flask(__name__)

@app.route('/songs/<songid>', methods=['GET'])
def get_song(songid):
    return songs.get_song(songid)

@app.route('/songs', methods=['GET'])
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

@app.route('/songs/pagecount', methods=['GET'])
def get_page_count():
    return songs.get_page_count()

@app.route('/songs/count', methods=['GET'])
def get_count():
    return songs.get_count()
    
app.run(debug=True)