import pandas as pd


def get_genre(genre, name):
    compare = 'genre_' + genre
    if name == compare:
        return 1.0
    return 0.0


def predict(model, data):
    d = pd.DataFrame(columns=('acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'liveness',
                              'loudness', 'speechiness', 'valence', 'genre_A Capella', 'genre_Alternative', 'genre_Anime', 'genre_Blues',
                              'genre_Childrens Music', 'genre_Classical', 'genre_Comedy',
                              'genre_Country', 'genre_Dance', 'genre_Electronic', 'genre_Folk',
                              'genre_Hip-Hop', 'genre_Indie', 'genre_Jazz', 'genre_Movie',
                              'genre_Opera', 'genre_Pop', 'genre_R&B', 'genre_Rap', 'genre_Reggae',
                              'genre_Reggaeton', 'genre_Rock', 'genre_Ska', 'genre_Soul',
                              'genre_Soundtrack', 'genre_World'))

    genre = data['genre']
    genre_ACapella = get_genre(genre, 'genre_A Capella')
    genre_Alternative = get_genre(genre, 'genre_Alternative')
    genre_Anime = get_genre(genre, 'genre_Anime')
    genre_Blues = get_genre(genre, 'genre_Blues')
    genre_ChildrensMusic = get_genre(genre, 'genre_Childrens Music')
    genre_Classical = get_genre(genre, 'genre_Classical')
    genre_Comedy = get_genre(genre, 'genre_Comedy')
    genre_Country = get_genre(genre, 'genre_Country')
    genre_Dance = get_genre(genre, 'genre_Dance')
    genre_Electronic = get_genre(genre, 'genre_Electronic')
    genre_Folk = get_genre(genre, 'genre_Folk')
    genre_HipHop = get_genre(genre, 'genre_Hip-Hop')
    genre_Indie = get_genre(genre, 'genre_Indie')
    genre_Jazz = get_genre(genre, 'genre_Jazz')
    genre_Movie = get_genre(genre, 'genre_Movie')
    genre_Opera = get_genre(genre, 'genre_Opera')
    genre_Pop = get_genre(genre, 'genre_Pop')
    genre_RB = get_genre(genre, 'genre_R&B')
    genre_Rap = get_genre(genre, 'genre_Rap')
    genre_Reggae = get_genre(genre, 'genre_Reggae')
    genre_Reggaeton = get_genre(genre, 'genre_Reggaeton')
    genre_Rock = get_genre(genre, 'genre_Rock')
    genre_Ska = get_genre(genre, 'genre_Ska')
    genre_Soul = get_genre(genre, 'genre_Soul')
    genre_Soundtrack = get_genre(genre, 'genre_Soundtrack')
    genre_World = get_genre(genre, 'genre_World')

    d.loc[0] = [data['acousticness'], data['danceability'], data['duration_ms'], data['energy'], data['instrumentalness'],
                data['liveness'], data['loudness'], data['speechiness'], data['valence'], genre_ACapella, genre_Alternative,
                genre_Anime, genre_Blues, genre_ChildrensMusic, genre_Classical, genre_Comedy,
                genre_Country, genre_Dance, genre_Electronic, genre_Folk, genre_HipHop,
                genre_Indie, genre_Jazz, genre_Movie, genre_Opera, genre_Pop, genre_RB, genre_Rap,
                genre_Reggae, genre_Reggaeton, genre_Rock, genre_Ska, genre_Soul, genre_Soundtrack, genre_World]

    pred = model.predict_proba(d)
    val0 = pred[0][0]
    val1 = pred[0][1]
    predicted_val = '1'
    confidence = val1
    if val1 < val0:
        predicted_val = '0'
        confidence = val0

    return {'result': predicted_val, 'confidence': confidence}
