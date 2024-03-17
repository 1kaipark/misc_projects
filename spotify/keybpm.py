import base64
import requests
import json

client_id = "e5a7fb4e507f4b83a942647e75961e84"
client_secret = "bea3ad93c3a64d34acf4fe4410fdeb5c"

def get_token():
    auth_string = f"{client_id}:{client_secret}"
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

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

# COMMON VARIABLES
ub_url = "https://api.spotify.com/v1"
token = get_token()

def search_for_track(token, track_name):
    url = f"{ub_url}/search"
    headers = get_auth_header(token)
    query = f"?q={track_name}&type=track&limit=1"
    query_url = f"{url}{query}"

    result = requests.get(query_url, headers = headers)
    json_result = result.json()
    return json_result['tracks']['items'][0]


def get_track_audio_features(token, track_id):
    url = f"{ub_url}/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = requests.get(url, headers = headers)
    json_result = result.json()
    return json_result

def get_bpm_key(token, track_id):
    audio_features = get_track_audio_features(token, track_id)
    bpm = audio_features['tempo']

    key_pitch_class = audio_features['key']
    to_notes = {
        0: "C",
        1: "C#/Db",
        2: "D",
        3: "D#/Eb",
        4: "E",
        5: "F",
        6: "F#/Gb",
        7: "G",
        8: "G#/Ab",
        9: "A",
        10: "A#/Bb",
        11: "B"
    }
    key = to_notes.get(key_pitch_class)

    return bpm, key

trackres = search_for_track(token, input("song? "))
id = trackres['id']
name = trackres['name']

bpm, key = get_bpm_key(token, id)
print(f"{name} : {bpm} BPM {key}")