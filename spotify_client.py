#A cli program for searching in Spotify playlists
#Lots of help from CodingEntrepeneurs for the SpotifyAPI class
#(video at https://www.youtube.com/watch?v=xdq6Gz33khQ)
#Step 1: connect to Spotify web api
import base64
import datetime
from urllib.parse import urlencode

import requests
import webbrowser

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    oauth_token = None
    user_id = None
    token_url = "https://accounts.spotify.com/api/token"
    def __init__(self, client_id, client_secret, oauth_token, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret
        self.oauth_token = oauth_token
        self.user_id = user_id
        #######Version ID, update for future Spotify API versions
        self.version = 'v1'
    ###Methods for obtaining and passing credentials to Spotify API
    def get_client_credentials(self):
        #Returns a base64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }
    #TODO: modularize perform_auth
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200,299):
            raise Exception("Could not authenticate client.")
            #return False
        data = r.json()
        now = datetime.datetime.now()
        self.access_token = data['access_token']
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers
    def get_user_header(self):
        oauth_token = self.oauth_token
        headers = {
            "Authorization": f"Bearer {oauth_token}"
        }
        return headers
    ###Get methods for different search criteria
    def get_resource(self, lookup_id, resource_type='albums'):
        endpoint = f"https://api.spotify.com/{self.version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    ###Following methods take an id string as an argument and return
    ###the result in human form
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')
    def get_track(self, _id):
        return self.get_resource(_id, resource_type='tracks')
    def get_user(self, _id):
        return self.get_resource(_id, resource_type='users')
    def get_playlists(self, _id):
        endpoint = f"https://api.spotify.com/{self.version}/users/{_id}/playlists?limit=50"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    ########################BETA SHIT##############################
    ## won't work without logging in...
    def get_my_playlists(self):
        endpoint = f"https://api.spotify.com/{self.version}/users/{self.user_id}/playlists?limit=50"
        headers = self.get_user_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    ##let's take a crack at logging in and looking at playlists
    ####DO NOT USE THIS FUNCTION YET!! #########
    def user_login(self):
        #first have user authenticate with GET request
        ##this won't work. Would be great for like a web app, not so much for Python
        ##Instead, hardcode my user token for now, figure out how to do this when
        ##converting to Android app or web app
        endpoint = "https://accounts.spotify.com/authorize"
        headers = self.get_resource_header()
        client_id = self.client_id
        response_type = "code"
        redirect_uri = "https://google.ca/" #no real significance to redirect, randomly chose google
        state = "xyz"
        scope = "playlist-read-collaborative%20playlist-read-private"
        r = requests.get(endpoint, params={"client_id":client_id,"response_type":response_type,"redirect_uri":redirect_uri,"state":state,"scope":scope},headers=headers)
        webbrowser.open(r.url,new=2)
        #now make POST request to grab code and state
        url = "https://accounts.spotify.com/api/token"

        return r.url
    ########################END BETA ##############################
    ###Search methods
    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = "%20".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "and":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)
    def get_playlist_tracks(self, play_id):
        endpoint = f"https://api.spotify.com/{self.version}/playlists/{play_id}/tracks"
        headers = self.get_user_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200,299):
            return {}
        return r.json()
#############Totally copied all of the above from CodingEntrepeneurs##########
