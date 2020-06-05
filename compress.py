import gzip
import shutil
with open('songs.db', 'rb') as f_in:
    with gzip.open('songs.db.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)