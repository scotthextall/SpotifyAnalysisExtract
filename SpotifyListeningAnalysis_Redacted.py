import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt

# Spotify API authentication and setting query scope
client_id = "redacted"
client_secret = "redacted"
sp_api = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:3000", scope="user-read-recently-played"))

# Get listening history - API limit 50, but can overcome by querying in batches (not included in this extract due to 30 line limit)
listening_history = sp_api.current_user_recently_played(limit=50)

# Create 2D array to store day_of_week (7 rows) and hour_of_day (24 columns) data
history_heatmap = np.zeros((7, 24))

# Extract day and hour data of when each listen happened from listening_history. Store in history_heatmap
for item in listening_history["items"]:
    played_at = dt.strptime(item["played_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
    day_of_week = played_at.weekday()
    hour_of_day = played_at.hour
    history_heatmap[day_of_week][hour_of_day] += 1

plt.figure(figsize=(8, 5))
heatmap = plt.imshow(history_heatmap, cmap="YlGnBu", aspect="auto")
plt.colorbar(heatmap, label="Number of listens")
plt.xlabel("Hour of the day"), plt.ylabel("Day of the week"), plt.title("No. Listens per Day of the Week and Hour of the Day over Past 50 Listens")
plt.xticks(np.arange(0, 24, 1)), plt.yticks(np.arange(0, 7, 1), ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
plt.show()