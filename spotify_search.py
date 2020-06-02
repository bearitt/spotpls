from spotify_client import *

#Step 2: get access token from user credentials
client_id = '1db86c161cf5402a8bc1c33628945937'
client_secret = '7d29652404bb482b8dda5d84588f5584'

spotify = SpotifyAPI(client_id,client_secret)
print(spotify.search("Kenny", search_type="artist"))
#might go off the rails from here on...
#sample code for searching for a track name:
'''headers = {
    "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q": "Time", "type": "track"})
lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=headers)
print(r.json())
'''



#Step 3: Get input from user
#########################################################################
#####################Search requested####################################
#Step 4a: Get playlist name and search term from user
#Step 4b: Get list of songs in playlist
#Step 4c: Compare search terms to playlist dict (song titles, album titles, artist names)
#Step 4d: Return search results to user
#########################################################################
#####################Help requested######################################
#Step 4: Return list of commands to user
#########################################################################
#####################WORK IN PROGRESS...#################################
