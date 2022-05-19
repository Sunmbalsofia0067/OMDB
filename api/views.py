from django.shortcuts import render
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .models import Movie
from .serializers import MovieSerializer
from django.db.models import Q
from django.contrib.auth.models import User



def index(request):
    data = Movie.objects.all()
    return render(request, 'index.html', {'data': data})



class MovieAPIView(APIView):

    def get(self, request):

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        offset = limit * (page-1)
        movies = Movie.objects.all().order_by('title')[offset:offset+limit].values()
        return Response(movies)


class MovieSearchAPIView(APIView):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]

    def get(self, request):

        title = request.GET.get('title')
        id = request.GET.get('id')

        movies = Movie.objects.filter(Q(id = id) | Q(title = title)).values()

        if not movies:
            return Response("No record found.")

        return Response(movies)



class MovieDeleteAPIView(APIView):

    def delete(self, request,  *args, **kwargs):
        user = request.user
        if self.delete_permision(user): 
            try:
                id = kwargs.get('id')
                movie = Movie.objects.get(id=id)
                title = movie.title
                movie.delete()
                return Response("{} movie has been deleted.".format(title))
            except:
                return Response("Movie doesn't exist.")
        
        else:
            return Response("This user doesn't have right to delete a record.")


    def delete_permision(self, user):
        if 'api.delete_movie' in user.get_user_permissions():
            return True
        else:
            return False


class SyncMovieView(APIView):

    def get(self, request):

        search_title = request.GET.get('title', '')

        if not search_title:
            return Response("Please enter title.")

        current_keyword_index = 0
        records = []

        page = 1
        while True:
            omdbapi_resp = requests.get('https://www.omdbapi.com/?s={}&apikey=43405bc5&type=movie&page={}'.format(search_title, page))
            omdbapi_resp = omdbapi_resp.json()

            if omdbapi_resp['Response'] == "True":
                records = records + omdbapi_resp["Search"]
                page += 1
            
            elif omdbapi_resp['Response'] == "False":
                break

        for record in records:
            Movie(
                title = record['Title'],
                year = record['Year'],
                imdb_id = record['imdbID'],
                type = record['Type'],
                poster = record['Poster']
            ).save()

        response = {
            'totalMoviews': len(records),
            'searchTitle': search_title,
            'movies': records
        }
        return Response(response)
