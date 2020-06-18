import pandas as pd
import zipfile
import io
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

def prep_data(text):
    print('received data')
    io_data = io.StringIO(text)
    df = pd.read_csv(io_data)
    df = clean_df(df)
    print('cleaned data')
    labels = pd.DataFrame()
    labels['target'] = df.apply(lambda row: is_popular(row, df['popularity'].mean()), axis=1)
    print('label targets generated')
    df = transform_min_max(df)
    print('min-maxed features')
    
    io_f = io.StringIO()
    io_l = io.StringIO()
    df.to_csv(io_f)
    labels.to_csv(io_l)

    print('csv files created')
    zipped_file = io.BytesIO()
    with zipfile.ZipFile(zipped_file, 'w') as z:
        z.writestr('features.csv', io_f.getvalue())
        z.writestr('labels.csv', io_l.getvalue())
    
    zipped_file.seek(0)
    print('csv files zipped')
    return zipped_file