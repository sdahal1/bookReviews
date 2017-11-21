from django.conf.urls import url #import
from . import views
#THIS IS THE URLS.PY FOR APPS.MAIN

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.createUser),
    url(r'^login$', views.login),
    url(r'^books$', views.indexBook),
    url(r'^logout$', views.logout),
    url(r'^books/new$', views.newBook),
    url(r'^reviews$', views.createBookReview),
    url(r'^books/(?P<id>\d+)$', views.showBook), 
    url(r'^reviews/(?P<id>\d+)/delete$', views.deleteReview),
    url(r'^reviews/(?P<id>\d+)$', views.createReview),
    url(r'^users/(?P<id>\d+)$', views.showUser)
]