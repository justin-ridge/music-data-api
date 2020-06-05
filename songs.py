import db
import json
import math

PAGE_SIZE = 50

def get_songs(page):
    return get_songs_query('', page)

def get_song(songid):
    query = db.query_db('SELECT * FROM songs WHERE songid=%s;' % songid)
    return json.dumps(query)

def get_page_count():
    count = int(get_count())
    return str(math.ceil(count / PAGE_SIZE))

def get_count():
    query = query = db.query_db('SELECT COUNT(*) FROM songs')
    return str(query[0].get('COUNT(*)'))

def get_songs_features(page):
    return get_songs_query('JOIN features f ON s.songid=f.songid', page)

def get_songs_minmax(page):
    return get_songs_query('JOIN minmax m ON s.songid=m.songid', page)

def get_songs_query(join, page):
    offset = int(page) * PAGE_SIZE
    query = db.query_db('SELECT * FROM songs s %s LIMIT %d OFFSET %d;' % (join, PAGE_SIZE, offset))
    return json.dumps(query)
