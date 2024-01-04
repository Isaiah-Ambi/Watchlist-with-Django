from django.shortcuts import render, redirect
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
        print(show_data)
        shows = []
        for show in show_data:
            shows.append({
                'name': show['show']['name'],
                'id': show['show']['id'],
                'image': show['show']['image']['medium']
            })
        # shows = show_data['show']

        # Render template with show results
        return render(request, 'watchlist/search_results.html', {'shows': shows})

    else:
        return render(request, 'watchlist/search_form.html')
