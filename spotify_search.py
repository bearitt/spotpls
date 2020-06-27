from spotify_client import *
import json
from secrets import *
#Step 1: get access token from user credentials

spotify = SpotifyAPI(client_id,client_secret,oauth_token,user_id)

#Step 2: Get playlist search term from user
search = input("Enter a playlist search term: ")
#Step 3: Show a list of playlists matching search term
playlist_json = spotify.get_my_playlists()
playlist_match = []
for item in playlist_json["items"]:
    if item["name"].lower().find(search.lower()) != -1:
        playlist_match.append(item)
print("Search results:")
print("------------------------")
i = 1
for plist in playlist_match:
    print(str(i) + ": " + plist["name"])
    i += 1
pl_select = int(input("Please enter playlist to export: "))
while pl_select >= i or pl_select < 1:
    print("Invalid selection, try again.")
    pl_select = input("Please enter playlist to export: ")

#Step 4b: Get list of songs in playlist
tracks_json = spotify.get_playlist_tracks(playlist_match[pl_select - 1]["id"])
i = 1
print("--------------------------")
for track in tracks_json["items"]:
    print("Track number " + str(i))
    i += 1
    print("Artist:\t\t" + track["track"]["album"]["artists"][0]["name"])
    print("Track name:\t" + track["track"]["name"])

    print("--------------------------")
    #for thing in item["track"]:
    #    print(thing)
'''
for track in tracks_json["items"]:



'''


#Step 4c: Compare search terms to playlist dict (song titles, album titles, artist names)
#Step 4d: Return search results to user
#########################################################################
#####################Help requested######################################
#Step 4: Return list of commands to user
#########################################################################
#####################WORK IN PROGRESS...#################################


#Sample code: Search for playlists by username
'''
playlist_json = spotify.get_playlists('2244p5ucgdja7d45qxhzwkxsa')
ps_items = playlist_json['items']
for item in ps_items:
    print(item['name'] + "\tCollaborative: " + str(item['collaborative']))
print(len(ps_items))
'''
##Sample code: print only collaborative playlists
'''
playlist_json = spotify.get_my_playlists()
for item in playlist_json["items"]:
    if item["collaborative"] == True:
        print(item["name"])
print("Done")
'''
#Sample code: search for a track name:
'''
headers = {
    "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q": "Time", "type": "track"})
lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=headers)
print(r.json())
'''
