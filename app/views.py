from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth import logout

from .forms import RegisterForm
from .models import Film

# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')

def signout(request):
    logout(request)
    return redirect(reverse_lazy('login'))

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)
    
class FilmList(ListView):
    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        user = self.request.user
        return user.films.all()
    
def add_film(request):
    # Get film name entered from form 
    name = request.POST.get('filmname')
    # Create film object with the entered name 
    film = Film.objects.create(name=name)

    # Add the user to the film 
    request.user.films.add(film)

    # Retrive all the user's films 
    films = request.user.films.all()

    # Return template fragment with user's films
    return render(request, 'partials/film-list.html', {'films': films})

def delete_film(request, film_id):
    # Remove the film from user's list
    request.user.films.remove(film_id) 

    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

    
def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">This username already exists</div>')
    else:
        return HttpResponse('<div id="username-error" class="success">This username is available</div>')
