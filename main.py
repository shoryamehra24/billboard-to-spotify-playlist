from os import name
import requests
from bs4 import BeautifulSoup
import lxml
from pprint import pprint
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyOAuth
from data import CLIENT_ID, REDIRECT_URI, CLIENT_SECRET



year = input("To what year do wish to be transported to? ")

URL = f"https://www.billboard.com/charts/year-end/{year}/hot-100-songs"

response = requests.get(url=URL)
content = response.text

soup = BeautifulSoup(content, 'lxml')
song_tags = soup.find_all(name='div', class_="ye-chart-item__title")
song_names = []

for tag in song_tags:
    song_name = tag.getText().strip()
    song_names.append(song_name)

auth = SpotifyOAuth(client_id= CLIENT_ID,
                    client_secret= CLIENT_SECRET,
                    redirect_uri= REDIRECT_URI,
                    scope= 'playlist-modify-private',
                    cache_path= 'token.txt')

# auth.get_access_token()

auth_token = auth.get_cached_token()['access_token']


user_id = Spotify(auth_token).me()['id']
print(user_id)

song_uris = []

for name in song_names:
    try:
        song_uri = Spotify(auth_token).search(q=name, type='track')['tracks']['items'][3]['uri']
        song_uris.append(song_uri)
    except KeyError:
        continue

new_playlist = Spotify(auth_token).user_playlist_create(user=user_id,
                                                           name=f"Best of {year}",
                                                           public= False,
                                                           description= f"The best songs of {year}." )


add_songs = Spotify(auth_token).playlist_add_items(playlist_id=new_playlist['id'],
                                                   items=song_uris,
                                                   position=None)

print("Playlist has been created. Enjoy!")