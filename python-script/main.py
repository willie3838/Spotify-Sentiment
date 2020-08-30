import spotipy
from spotipy.oauth2 import SpotifyOAuth
import sys
import nltk
import re
import textblob



def cleanData(text: str) -> str:
    text = text.lower()
    # removes anything that's not in the set of a-z
    text = re.sub('[^a-z\s]','',text)
    # tokenize sentence into words then remove stop words
    text = nltk.word_tokenize(text)
    stop_words = nltk.corpus.stopwords.words('english')
    text = [w for w in text if w not in stop_words]
    # lemmatizes the words
    text = [nltk.stem.WordNetLemmatizer().lemmatize(w, pos="v") for w in text]
    text = " ".join(text)

    return text

# basic sentiment analysis with textblob
def sentimentAnalysis(text):
    blob = textblob.TextBlob(text)
    return blob.sentiment


### SETTING UP CREDENTIALS FOR SPOTIFY ###
def spotifySetup() -> spotipy:
    scope = "user-library-read user-read-private user-read-playback-state user-modify-playback-state"
    # username: eeu7lilkr2jl6ji6xf0kq9dyj

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit()

    client_credentials_manager = SpotifyOAuth(username = username, scope=scope,client_id='f246cf20044545b4a0cc4be52df9b503',client_secret='6d10dbd5ddea4214aef14fd97a91152a',redirect_uri='http://localhost:8888/callback')
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


### Setting up sentiment analysis ###
print("How was your day today?")
sent = input()
sent = cleanData(sent)

sentiment = sentimentAnalysis(sent).polarity

### SPOTIFY SETUP #####
spotify = spotifySetup()
# getting device information
devices = spotify.devices()
deviceID = devices['devices'][0]['id']

if sentiment < 0:
    print("Hope this makes you feel better")
    spotify.start_playback(device_id=deviceID, context_uri="spotify:playlist:6czgPNzwlh7nCpVl5eOlX4")
else:
    print("Wow, you seem pumped. Let's keep this up")
    spotify.start_playback(device_id=deviceID, context_uri="spotify:playlist:3noGEnFdliB2FT6IP1h55G")

# getting track information
try:
    track = spotify.current_user_playing_track()
    artist = track['item']['artists'][0]['name']
    track = track['item']['name']

    if artist != "":
        print("Currently playing " + artist + " - " + track)
except:
    print("Currently playing no songs")