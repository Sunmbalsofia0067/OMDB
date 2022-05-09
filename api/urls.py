"""omdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import MovieAPIView, SyncMovieView, MovieSearchAPIView, MovieDeleteAPIView

urlpatterns = [
    path('all/', MovieAPIView.as_view()),
    path('sync/', SyncMovieView.as_view()),
    path('search/', MovieSearchAPIView.as_view()),
    path('delete/<int:id>/', MovieDeleteAPIView.as_view())

]
