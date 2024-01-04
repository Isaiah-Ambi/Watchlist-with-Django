from types import NoneType
from django.shortcuts import render, redirect
from .models import Show, WatchListShow
import requests
import json

# Create your views here.

def search_shows(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')

        # Send API request to TVMaze
        url = f"https://api.tvmaze.com/search/shows?q={search_query}"
        response = requests.get(url)

        # Parse response and extract show data
        show_data = response.json()
        shows = []
        #exception for nonetype element
        # if show_data == NoneType:
        #     shows = []
        # else:
        #     for show in show_data:
        #         shows.append({
        #             'name': show['show']['name'],
        #             'id': show['show']['id'],
        #             'image': show['show']['image']['medium'] if show['show']['image'] else 'No image'
        #         })
        # print(show_data)
        # shows = show_data['show']
        show = []
        for show in show_data:
            
            shows.append({
                'name': show['show']['name'],
                'id': show['show']['id'],
                'image': show['show']['image']['medium'] if show['show']['image'] else 'No image',
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
    
def add_to_watchlist(request, id):
    # Add show to watchlist
    url = f"https://api.tvmaze.com/lookup/shows?thetvdb={id}"
    response = requests.get(url)
    if response.status_code == 200:
        
        show_data = response.json()
        show = Show.objects.create(
            tvmaze_id=show_data['id'],
            name=show_data['name'],
            image_url=show_data['image']['medium'],
            summary=show_data['summary'],
            rating=show_data['rating']['average'],
            status=show_data['status'],
            genres=','.join(show_data['genres']),
            premiered=show_data['premiered'])
    else:
        return redirect('search')
    
def watchlist(request):
    watchlist_shows = WatchListShow.objects.filter(user=request.user)
    
    return render(request, 'watchlist/watchlist.html', {'watchlist_shows': watchlist_shows})
