from django.db.models import Max
from .models import UserFilms

def get_max_order(user):
    # Get the user's existing films 
    existing_films = UserFilms.objects.filter(user=user)
    # If no films exist for the user, return 1
    if not existing_films.exists():
        return 1
    else:
        current_max = existing_films.aggregate(max_order=Max('order'))['max_order']
        return current_max + 1
    

def reorder(user):
    # Get the user's existing films 
    existing_films = UserFilms.objects.filter(user=user)

    if not existing_films.exists():
        return
    
    number_of_films = existing_films.count()
    new_ordering = range(1, number_of_films+1)
    films = []

    for order, user_film in zip(new_ordering, existing_films):
        user_film.order = order
        films.append(user_film)
    UserFilms.objects.bulk_update(films, fields=['order'], batch_size=100)