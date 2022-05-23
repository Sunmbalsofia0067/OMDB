from django.test import RequestFactory, TestCase
from api.models import Movie
from django.contrib.auth.models import User
from api.views import *

class DatabaseTransactionTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title="test_title", year=1992, imdb_id="test_imdb_id", type="test_type", poster="test_poster")

    def test_database_transaction(self):
        movie = Movie.objects.get(title="test_title")
        self.assertEqual(movie.pk, 1)
        self.assertEqual(movie.year, 1992)
        self.assertEqual(movie.imdb_id, "test_imdb_id")
        self.assertEqual(movie.type, "test_type")
        self.assertEqual(movie.poster, "test_poster")

class UrlAndViewsTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title="test_title", year=1992, imdb_id="test_imdb_id", type="test_type", poster="test_poster")
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='jacob', email='', password='top_secret')

    def test_home_url_and_index_view(self):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)

    def test_Movie_Api_View(self):
        request = self.factory.get('/api/movie/all/')
        request.user = self.user
        response = MovieAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    
    def test_Sync_Movie_View(self):
        request = self.factory.get('/api/movie/sync/')
        request.user = self.user
        response = SyncMovieView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_Movie_Search_Api_View(self):
        request = self.factory.get('/api/movie/search/')
        request.user = self.user
        response = MovieSearchAPIView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_Movie_Delete_Api_View(self):
        request = self.factory.delete('/api/movie/delete/1')
        request.user = self.user
        response = MovieDeleteAPIView.as_view()(request)
        self.assertEqual(response.status_code, 403) #this code says browser understands your request but does not want to auhorize it
            
