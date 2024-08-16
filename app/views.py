from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

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


@login_required
@require_http_methods(['POST'])
def add_film(request):
    # Get film name entered from form 
    name = request.POST.get('filmname')
    # Create film object with the entered name 
    
    film = Film.objects.get_or_create(name=name)[0]

    # Add the user to the film 
    request.user.films.add(film)

    # Retrive all the user's films 
    films = request.user.films.all()
    
    messages.success(request, f"You've successfully added {name} to your list!")

    # Return template fragment with user's films
    return render(request, 'partials/film-list.html', {'films': films})

@login_required
@require_http_methods(['DELETE'])
def delete_film(request, film_id):
    
    # Remove the film from user's list
    request.user.films.remove(film_id) 

    films = request.user.films.all()
    return render(request, 'partials/film-list.html', {'films': films})

def search_film(request):
    search_text = request.POST.get('search')
    
    userfilms = request.user.films.all()
    results = Film.objects.filter(name__icontains=search_text).exclude(name__in=userfilms.values_list('name', flat=True))
    
    return render(request, 'partials/search-results.html', {'results': results})

    
def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">This username already exists</div>')
    else:
        return HttpResponse('<div id="username-error" class="success">This username is available</div>')
    
def clear(request):
    return HttpResponse("")
