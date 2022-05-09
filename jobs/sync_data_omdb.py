import requests
import sys
import os
import django

sys.path.append('../omdb/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_job")
sys.path.append('../')

django.setup()

from api.models import Movie


class OMDBDataSync:

    def __init__(self):
        self.keywords = ['begin', 'man', 'last', 'fight', 'love', 'night']
        self.data_limit = 100
        self.api_url = 'https://www.omdbapi.com/?s={}&apikey=43405bc5&type=movie&page={}'


    def sync(self):        
        if not Movie.objects.all().exists():
            current_keyword_index = 0
            records = []

            page = 1

            while len(records) < self.data_limit:
                omdbapi_resp = requests.get(self.api_url.format(self.keywords[current_keyword_index], page))
                omdbapi_resp = omdbapi_resp.json()

                if omdbapi_resp['Response'] == "True":
                    records = records + omdbapi_resp["Search"]
                    page += 1
                
                elif omdbapi_resp['Response'] == "False":
                    if len(records) < self.data_limit:
                        current_keyword_index += 1
                        page = 1

            records = records[:self.data_limit]
            self.save_data_db(records)

            result = {
                'totalMovies': len(records),
                # 'movies': records
            }
            print(result)

        else:
            print('Database has already been populated.')


    def save_data_db(self, data):
        for d in data:
            Movie(
                title = d['Title'],
                year = d['Year'],
                imdb_id = d['imdbID'],
                type = d['Type'],
                poster = d['Poster']
            ).save()


if __name__ == "__main__":
    syncer = OMDBDataSync()
    syncer.sync()