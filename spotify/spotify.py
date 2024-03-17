import base64
import requests
import json
from urllib.parse import quote
import webbrowser



# COMMON VARIABLES
ub_url = "https://api.spotify.com/v1"

class Spotify:
    def __init__(self, client_id, client_secret, redrect_uri = None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redrect_uri

    def get_token(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization" : "Basic " + auth_base64,
            "Content-Type" : "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type" : "client_credentials"
        }

        result = requests.post(url, headers = headers, data = data)
        json_result = json.loads(result.content)
        return json_result['access_token']

    def get_auth_header(self, token):
        return {"Authorization" : "Bearer " + token}

    def get_authcode(self):
        encoded_rduri = quote(self.redirect_uri)

        scopes = [
            "user-follow-read",
            "user-top-read",
            "user-read-private",
            "user-read-email"
        ]


        encoded_scopes = quote((' '.join(scopes)).strip())

        auth_url = f"https://accounts.spotify.com/authorize?client_id={self.client_id}&response_type=code&redirect_uri={self.encoded_rduri}&scope={encoded_scopes}"
        webbrowser.open(auth_url)

        print("After granting permission, you will be redirected to your redirect URI with a code in the query string.")
        print("Paste the full redirect URI here: ")
        redirected_uri = input()

        # Extract the code from the redirected URI
        code = redirected_uri.split("code=")[1].split("&")[0]

        return code

    def get_token_authcode(self, code):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization" : "Basic " + auth_base64,
            "Content-Type" : "application/x-www-form-urlencoded",
        }
        data = {
            "grant_type" : "authorization_code",
            "code": code,
            "redirect_uri" : self.redirect_uri
        }
        result = requests.post(url, headers = headers, data = data)
        json_result = result.json()
        return json_result['access_token']
