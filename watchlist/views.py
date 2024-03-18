from types import NoneType
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, WatchListShowForm, CustomListForm
from .models import Show, WatchListShow, CustomList
import requests


# Create your views here.
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after registration
            return redirect('search')  # Redirect to the homepage or any other page
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'base/profile.html')

def search_shows(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')

        # Send API request to TVMaze
        url = f"https://api.tvmaze.com/search/shows?q={search_query}"
        response = requests.get(url)

        # Parse response and extract show data
        show_data = response.json()
        shows = []

        show = []
        for show in show_data:
            
            shows.append({
                'name': show['show']['name'],
                'tvmaze_id': show['show']['id'],
                'image_url': show['show']['image']['medium'] if show['show']['image'] else 'No image',
                'summary': show['show']['summary'],
                'rating': show['show']['rating']['average'],
                'status': show['show']['status'],
                'genres': show['show']['genres'],
                'premiered': show['show']['premiered'],
            })
            
        # shows = show_data['show']

        # Render template with show results
        return render(request, 'watchlist/search_results.html', {'shows': shows})
    else:
        return render(request, 'watchlist/search_form.html')
@login_required
def watchlist(request):
    watchlist = WatchListShow.objects.filter(user=request.user)
    return render(request, 'watchlist/watchlist.html', {'watchlist': watchlist})


def add_to_watchlist(request, id):

    try:
        show = Show.objects.get(tvmaze_id=id)
    except Show.DoesNotExist:
    # Show not found, create a new one
        url = f"https://api.tvmaze.com/shows/{id}"
        response = requests.get(url)
        show_data = response.json()
        show = Show.objects.create(
            tvmaze_id = show_data['id'],
            name = show_data['name'],
            genres = show_data['genres'],
            status = show_data['status'],
            image_url = show_data['image']['medium'] if show_data['image'] else 'No image',
            premiered = show_data['premiered'],
            rating = show_data['rating']['average'],
            summary = show_data['summary'],
        )

    try:
        watchlist_show = WatchListShow.objects.get(user=request.user, show=show)
        message = f"'{show.name}' show already exists in your watchlist."
    except WatchListShow.DoesNotExist:
            watchlist_show = WatchListShow.objects.create(
                user=request.user,
                show=show,
                watch_status="TO_WATCH",
            )
            message = f"'{show.name}' added to your watchlist."

            context = {
                'message': message,
            }
            return render(request, 'watchlist/add_show_to_watchlist.html', context)

    except requests.exceptions.RequestException as e:
        # Handle API errors ...
        return render(request, 'watchlist/add_show_to_watchlist.html', {'error_message': "Error retrieving show information. Please try again."})

    return redirect('search')

# remove show from user watchlist
def remove_from_watchlist(request, id):
    try:
        watchlist_show = WatchListShow.objects.get(user=request.user, id=id)
        watchlist_show.delete()
        message = f"'{watchlist_show.show.name}' removed from your watchlist."
        context = {
            'message': message,
        }
        return render(request, 'watchlist/add_show_to_watchlist.html', context)
    except WatchListShow.DoesNotExist:
        context = {
            'error_message': "Show not found in your watchlist."
        }
        return render(request, 'watchlist/add_show_to_watchlist.html', context)
    
# update watch_status
def update_show_watch_status(request, id):
    try:
        watchlist_show = WatchListShow.objects.get(user=request.user, id=id)

        # Handle form submission for updating watch status
        if request.method == 'POST':
            form = WatchListShowForm(request.POST, instance=watchlist_show)
            if form.is_valid():
                form.save()
                message = f"'{watchlist_show.show.name}' watch status updated!"
                context = {
                    'message': message,
                }
                return render(request, 'watchlist/add_show_to_watchlist.html', context)
        else:
            # Initialize form with current watch status
            form = WatchListShowForm(instance=watchlist_show)

        context = {
            'form': form,
            'show': watchlist_show.show,
        }
        return render(request, 'watchlist/update_watch_status.html', context)

    except WatchListShow.DoesNotExist:
        # Handle show not found in watchlist
        context = {
            'error_message': "Show not found in your watchlist.",
        }
        return render(request, 'watchlist/add_show_to_watchlist.html', context)

    
@login_required
def list_custom_lists(request):
    user_lists = CustomList.objects.filter(user=request.user)
    context = {'user_lists': user_lists}
    return render(request, 'your_template/list_custom_lists.html', context)

@login_required
def create_custom_list(request):
    if request.method == 'POST':
        form = CustomListForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.user = request.user
            list.save()
            return redirect('list_custom_lists')
    else:
        form = CustomListForm()
    context = {'form': form}
    return render(request, 'your_template/create_custom_list.html', context)


def show_details(request, id):
    show = WatchListShow.objects.get(pk=id, user=request.user)
    context = {'watchlist_show': show}
    return render(request, 'watchlist/show_details.html', context)
