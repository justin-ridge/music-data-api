import gzip
import shutil

def compress_db():
    with open('songs.db', 'rb') as f_in:
        with gzip.open('songs.db.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def unzip_db():
    with gzip.open('songs.db.gz', 'rb') as f_in:
        with open('songs.db', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)