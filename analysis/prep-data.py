import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def clean_df(df):
    df = df.drop(['artist_name','track_name','track_id','key','mode','time_signature'],axis=1)
    dummies = pd.get_dummies(df['genre']).rename(columns=lambda x: 'genre_' + str(x))
    df = pd.concat([df, dummies], axis=1)
    df = df.drop(['genre'],axis=1)
    return df

def transform_min_max(df):
    df = df.drop(['popularity'],axis=1)
    features=list(df.columns)
    data = df[features]
    mms = MinMaxScaler()
    mms.fit(data)
    data_transformed = mms.transform(data)
    data_transformed = pd.DataFrame(data_transformed,columns=df.columns)
    return data_transformed

def is_popular(item, popularity):
    if item['popularity'] >= popularity:
        return 1
    return 0

def prep_data(df):
    df = clean_df(df)
    labels = pd.DataFrame()
    labels['target'] = df.apply(lambda row: is_popular(row, df['popularity'].mean()), axis=1)
    df = transform_min_max(df)
    df.to_csv('features.csv')
    labels.to_csv('labels.csv')

df = pd.read_csv('spotify_features.csv')
prep_data(df)