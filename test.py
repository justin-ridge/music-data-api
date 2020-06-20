import unittest
import songs
import datamanipulation
import os
import json

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestDataManipulation(unittest.TestCase):

    def test_random_forest(self):
        filename = os.path.join(THIS_DIR, 'sample_0.csv')
        data = ''
        with open(filename, encoding='utf8') as file1:
            data = file1.read()

        result = datamanipulation.random_forest(data)
        self.assertFalse(result is None)
        self.assertEqual('0.828', str(round(result['score'], 3)))
        self.assertEqual(17500, result['trainedFields'])
        self.assertEqual(7500, result['testedFields'])
        self.assertEqual(1289, result['mislabeled'])


class TestSongs(unittest.TestCase):

    def test_get_songs(self):
        result = json.loads(songs.get_songs('0'))
        self.assertFalse(result is None)
        self.assertEqual(50, len(result))

    def test_get_count(self):
        result = songs.get_count()
        self.assertEqual('232725', result)

    def test_get_page_count(self):
        result = songs.get_page_count()
        self.assertEqual('4655', result)

    def test_get_song(self):
        result = json.loads(songs.get_song('500'))
        song = result[0]
        self.assertEqual(500, song['songid'])
        self.assertEqual('Chorus', song['artist'])
        self.assertEqual('Goin Up', song['name'])
        self.assertEqual('Movie', song['genre'])
        self.assertEqual(0, song['target'])

    def test_get_songs_metadata(self):
        minmax = json.loads(songs.get_songs_minmax('0'))
        features = json.loads(songs.get_songs_features('0'))
        m1 = minmax[0]
        f1 = features[0]
        self.assertEqual(m1['artist'], f1['artist'])
        self.assertEqual(m1['name'], f1['name'])
        self.assertFalse('popularity' in m1.keys())
        self.assertEqual(40, f1['popularity'])

    def test_search(self):
        artist = 'foO FighteRs'
        result = json.loads(songs.search('', artist, ''))
        self.assertEqual(138, len(result))
        name = 'white limO'
        result = json.loads(songs.search(name, artist, ''))
        self.assertEqual(2, len(result))


if __name__ == '__main__':
    unittest.main()
