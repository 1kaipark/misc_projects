client_id = "e5a7fb4e507f4b83a942647e75961e84"
client_secret = "bea3ad93c3a64d34acf4fe4410fdeb5c"

import base64
import requests
import json
def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials"
    }

    result = requests.post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result['access_token']


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


# COMMON VARIABLES
ub_url = "https://api.spotify.com/v1"


# functions for tracks
def search_for_track(token, track_name):
    url = f"{ub_url}/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    query_url = f"{url}{query}"

    result = requests.get(query_url, headers=headers)
    json_result = result.json()
    return json_result['tracks']['items'][0]


def get_audio_features(token, track_id):
    url = f"{ub_url}/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers=headers)
    json_result = result.json()
    return json_result


def get_recommendations(token, features, n_recommendations=10, exclude_features=[]):
    features_types = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'instrumentalness', 'liveness', 'valence', 'tempo', 'type', 'id', 'uri', 'track_href',
                      'analysis_url', 'duration_ms', 'time_signature']

    exclude_features.extend(['id', 'type', 'track_href', 'analysis_url'])
    # 'https://api.spotify.com/v1/recommendations?
    url = f"{ub_url}/recommendations"
    query = f"?seed_tracks={features['id']}&limit={n_recommendations}"
    query_ext = ""

    other_features = []
    for f, v in features.items():
        if f not in exclude_features:
            query_ext += f"&target_{f}={v}"

    headers = get_auth_header(token)
    result = requests.get(f"{url}{query}{query_ext}", headers=headers)
    json_result = result.json()
    return json_result


def clean_recommendations(json_result):
    recommendations = {}
    for tr in json_result['tracks']:
        recommendations[f"{tr['artists'][0]['name']} - {tr['name']}"] = tr['preview_url']
    return recommendations


search_q = input("track to search recommendations for: ")
n_recs = input("number of recommendations: ")
token = get_token()
track = search_for_track(token, str(search_q))['id']
features = get_audio_features(token, track)
r = get_recommendations(token, features, n_recommendations = n_recs)
recs = clean_recommendations(r)

for track, link in recs.items():
    print(f"track: {track}, preview link: {link} \n")
