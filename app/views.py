from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .forms import RegisterForm
from .models import Film, UserFilms
from .utility import get_max_order, reorder

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
    context_object_name = 'userfilms'

    def get_queryset(self):
        return UserFilms.objects.filter(user=self.request.user)


@login_required
@require_http_methods(['POST'])
def add_film(request):
    # Get film name entered from form 
    name = request.POST.get('filmname')
    # Create film object with the entered name 
    
    film = Film.objects.get_or_create(name=name)[0]

    # Add the user to the film
    if not UserFilms.objects.filter(user=request.user, film=film).exists():
        UserFilms.objects.create(user=request.user, film=film, order=get_max_order(request.user))

    # Retrieve all the user's films
    films = UserFilms.objects.filter(user=request.user)
    
    messages.success(request, f"You've successfully added {name} to your list!")

    # Return template fragment with user's films
    return render(request, 'partials/film-list.html', {'userfilms': films})

@login_required
@require_http_methods(['DELETE'])
def delete_film(request, userfilm_id):
    
    # Remove the film from user's list
    UserFilms.objects.get(id=userfilm_id).delete()

    # Send to reorder function 
    reorder(request.user)

    films = UserFilms.objects.filter(user=request.user)
    return render(request, 'partials/film-list.html', {'userfilms': films})

def search_film(request):
    search_text = request.POST.get('search')
    
    userfilms = UserFilms.objects.filter(user=request.user)
    results = Film.objects.filter(name__icontains=search_text).exclude(name__in=userfilms.values_list('film__name', flat=True))
    
    return render(request, 'partials/search-results.html', {'results': results})

    
def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username=username).exists():
        return HttpResponse('<div id="username-error" class="error">This username already exists</div>')
    else:
        return HttpResponse('<div id="username-error" class="success">This username is available</div>')
    
def clear(request):
    return HttpResponse("")

def sort(request):
    film_ids_order = request.POST.getlist('film_order')
    # print(film_ids_order)
    films = []
    for index, film_id in enumerate(film_ids_order):
        userfilm = UserFilms.objects.get(id=film_id)
        userfilm.order = index + 1
        # userfilm.save()
        films.append(userfilm)
    UserFilms.objects.bulk_update(films, fields=['order'], batch_size=100)
    
    context = {
        'userfilms': films
    }

    return render(request, 'partials/film-list.html', context)

@login_required
def detail(request, userfilm_id):
    userfilm = get_object_or_404(UserFilms, id=userfilm_id)
    
    context = {
        'userfilm': userfilm
    }
    return render(request, 'partials/film-detail.html', context)

@login_required
def films_partial(request):
    films = UserFilms.objects.filter(user=request.user)
    
    return render(request, 'partials/film-list.html', {'userfilms': films})

def upload_photo(request, userfilm_id):
    userfilm = get_object_or_404(UserFilms, id=userfilm_id)
    photo = request.FILES.get('photo')
    
    # Saving an image field 
    userfilm.film.photo.save(photo.name, photo)
    context = {
        'userfilm': userfilm
    }
    return render(request, 'partials/film-detail.html', context)