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
    query = db.query_db(
        'SELECT * FROM songs s %s  ORDER BY artist, name LIMIT %d OFFSET %d;' % (join, PAGE_SIZE, offset))
    return json.dumps(query)


def get_search_query(val, table):
    if len(val) < 3:
        return ''

    return '%s LIKE \'%%%s%%\'' % (table, val)


def get_where_clause(q1, q2, q3):
    query = 'WHERE '
    queries = []
    if len(q1) > 0:
        queries.append(q1)
    if len(q2) > 0:
        queries.append(q2)
    if len(q3) > 0:
        queries.append(q3)

    separator = ' AND '
    return query + separator.join(queries)


def search(name, artist, genre):
    name_query = get_search_query(name, 'name')
    artist_query = get_search_query(artist, 'artist')
    genre_query = get_search_query(genre, 'genre')
    where_clause = get_where_clause(name_query, artist_query, genre_query)
    if len(where_clause) == 0:
        return json.dumps([])

    print(where_clause)
    query = db.query_db(
        'SELECT * FROM SONGS s JOIN features f ON s.songid=f.songid %s ORDER BY artist, name LIMIT 200' % where_clause)
    return json.dumps(query)
