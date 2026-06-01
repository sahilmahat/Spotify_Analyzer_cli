# Spotify Listening Profile

A Python CLI tool that connects to Spotify and shows your listening profile — top tracks, most-played artists, release year breakdown, and track stats.

## What it does

- Fetches your top 20 tracks (last 6 months)
- Fetches your top 20 artists
- Counts most-repeated artists and genres
- Shows release year breakdown
- Calculates avg track length and explicit %

## Tech used

- Python 3
- `spotipy` — Spotify Web API client
- `python-dotenv` — for managing API credentials
- OAuth 2.0 — for Spotify authentication

## How to run

### 1. Create a Spotify Developer app

1. Go to https://developer.spotify.com/dashboard
2. Click **Create app**
3. Set redirect URI to `http://127.0.0.1:8888/callback`
4. Save and copy your **Client ID** and **Client Secret**

### 2. Clone and set up the project

```bash
git clone https://github.com/sahilmahat/spotify-mood.git
cd spotify-mood

python3 -m venv venv
source venv/bin/activate

pip install spotipy python-dotenv
```

### 3. Add your credentials

Create a `.env` file in the project folder:

SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback

### 4. Run

```bash
python3 app.py
```

The first time you run it, a browser window opens for Spotify login. After you allow access, the script runs and prints your listening profile.

## Sample output
