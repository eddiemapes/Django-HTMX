from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('signout/', views.signout, name='signout'),
    path("register/", views.RegisterView.as_view(), name="register"),
    path('films/', views.FilmList.as_view(), name='film-list'),
]

htmx_urlpatterns = [
    path('check_username/', views.check_username, name='check_username'),
    path('add-film/', views.add_film, name='add-film'),
]

urlpatterns += htmx_urlpatterns