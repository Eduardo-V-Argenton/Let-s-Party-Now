import requests, os
from django.contrib import messages
from datetime import datetime

TWITCH_CLIENT_ID = os.environ.get('TWITCH_CLIENT_ID')
TWITCH_CLIENT_SECRET = os.environ.get('TWITCH_CLIENT_SECRET')

# Function to get a new Twitch access token
def get_new_twitch_access_token():
    twitch_token_url = 'https://id.twitch.tv/oauth2/token'
    twitch_token_params = {
        'client_id': TWITCH_CLIENT_ID,
        'client_secret': TWITCH_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    response = requests.post(twitch_token_url, params=twitch_token_params)
    response.raise_for_status()
    return response.json()['access_token']

# Function to make a request to the IGDB API using the current access token
def get_igdb_data(request, data):
    access_token = request.session.get('igdb_access_token')
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=data)
    if response.status_code == 401:
        # If the access token is invalid or expired, get a new one and try again
        access_token = get_new_twitch_access_token()
        request.session['igdb_access_token'] = access_token
        headers['Authorization'] = f'Bearer {access_token}'
        response = requests.post('https://api.igdb.com/v4/games', headers=headers, data=data)
        if response.status_code != 200:
            messages.error(request, 'Ocorreu um erro, tente novamente')
            return -1
    elif response.status_code != 200:
        messages.error(request, 'Ocorreu um erro, tente novamente')
        return -1
    games = response.json()
    for game in games:
        if 'cover' in game:
            image_url = game['cover']['url']
            game['cover']['url'] = image_url.replace("t_thumb", "t_1080p")
        if 'first_release_date' in game:
            game['first_release_date'] = datetime.fromtimestamp(game['first_release_date']).strftime('%d/%m/%Y') 
    return games
