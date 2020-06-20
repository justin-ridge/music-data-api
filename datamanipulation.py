import pandas as pd
import zipfile
import io
import base64
from sklearn.preprocessing import MinMaxScaler
from data_container import DataContainer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

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

def get_clean_dataframes(data):
    print('received data')
    io_data = io.StringIO(data)
    df = pd.read_csv(io_data,index_col=0)
    df = clean_df(df)
    print('cleaned data')
    labels = pd.DataFrame()
    labels['target'] = df.apply(lambda row: is_popular(row, df['popularity'].mean()), axis=1)
    print('label targets generated')
    features = transform_min_max(df)
    print('min-maxed features')
    return DataContainer(features, labels)

def prep_data(data):
    data = get_clean_dataframes(data)
    
    io_f = io.StringIO()
    io_l = io.StringIO()
    data.features.to_csv(io_f)
    data.labels.to_csv(io_l)

    print('csv files created')
    zipped_file = io.BytesIO()
    with zipfile.ZipFile(zipped_file, 'w') as z:
        z.writestr('features.csv', io_f.getvalue())
        z.writestr('labels.csv', io_l.getvalue())
    
    zipped_file.seek(0)
    print('csv files zipped')
    return zipped_file

def naive_bayes(data):
    data = get_clean_dataframes(data)

    x_train, x_test, y_train, y_test = train_test_split(data.features, data.labels.values, train_size=0.7,test_size=0.3, random_state=101)
    model = GaussianNB()
    y_train = y_train.ravel()
    model.fit(x_train,y_train)
    y_pred = model.predict(x_test)
    score = model.score(x_test, y_test)

    return {
        'score': score, 
        'trainedFields': len(x_train),
        'testedFields': len(x_test),
        'mislabeled': str((y_test.ravel() != y_pred).sum())
    }

def get_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_importance(importance):
    fig = importance.nlargest(20).plot(kind='barh').get_figure()
    return get_image(fig)

def get_mean_pie(features):
    fig = features.mean().plot(kind='pie', figsize=(20, 16), fontsize=26).get_figure()
    return get_image(fig)

def get_target_count(labels):
    fig = labels['target'].value_counts().plot.bar().get_figure()
    return get_image(fig)

def random_forest(data):
    data = get_clean_dataframes(data)
    print(data.features.columns)
    print(data.labels.columns)

    x_train, x_test, y_train, y_test = train_test_split(data.features, data.labels.values, train_size=0.7,test_size=0.3, random_state=101)
    forest = RandomForestClassifier(max_depth = 10, min_samples_split=2, n_estimators = 100, random_state = 1)
    y_train = y_train.ravel()
    model = forest.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    score = model.score(x_test, y_test)
    importance = pd.Series(model.feature_importances_, index=data.features.columns)
    #print(importance)
    #dd = importance.to_dict()

    return {
        'score': score, 
        'trainedFields': len(x_train),
        'testedFields': len(x_test),
        'mislabeled': str((y_test.ravel() != y_pred).sum()),
        'images': {
            'importance': get_importance(importance),
            'mean': get_mean_pie(data.features),
            'labels': get_target_count(data.labels)
        }
    }