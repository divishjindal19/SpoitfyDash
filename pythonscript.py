import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

# ========== SET THESE ==========
CLIENT_ID = "c0b8e3b42b4d42ff9405308674d94fef"
CLIENT_SECRET = "e5b2103375de4645a9e15caa365e3f40"
csv_file = "spotify-2023.csv"  # Your dataset file
output_file = "spotify_with_urls.csv"
# ================================

# Setup Spotify API credentials
auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Load your dataset
df = pd.read_csv(csv_file, encoding='latin1')  # Adjust encoding if needed
df["spotify_url"] = ""
df["album_cover"] = ""

# Iterate and fetch info from Spotify
for idx, row in tqdm(df.iterrows(), total=len(df)):
    track_name = row["track_name"]
    artist_name = row["artist(s)_name"].split(",")[0]  # Take primary artist
    
    query = f"{track_name} {artist_name}"
    try:
        result = sp.search(q=query, type='track', limit=1)
        tracks = result.get("tracks", {}).get("items", [])
        if tracks:
            track = tracks[0]
            df.at[idx, "spotify_url"] = track["external_urls"]["spotify"]
            df.at[idx, "album_cover"] = track["album"]["images"][0]["url"]
    except Exception as e:
        print(f"Error at index {idx}: {e}")

# Save the updated DataFrame
df.to_csv(output_file, index=False)
print(f"Saved with URLs to {output_file}")
