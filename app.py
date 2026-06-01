import os
import spotipy
from collections import Counter
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()


def get_spotify_client():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URL"),
        scope="user-read-recently-played user-top-read"
    ))
    return sp


def get_top_tracks(sp, time_range="medium_term"):
    results = sp.current_user_top_tracks(limit=20, time_range=time_range)
    tracks = []
    for item in results["items"]:
        tracks.append({
            "name":        item.get("name", "Unknown"),
            "artist":      item["artists"][0].get("name", "Unknown"),
            "duration_ms": item.get("duration_ms", 0),
            "explicit":    item.get("explicit", False),
            "release":     item.get("album", {}).get("release_date", "0000")
        })
    return tracks


def get_top_artists(sp, time_range="medium_term"):
    results = sp.current_user_top_artists(limit=20, time_range=time_range)
    artists = []
    for item in results["items"]:
        artists.append({
            "name":   item.get("name", "Unknown"),
            "genres": item.get("genres", [])
        })
    return artists


def analyze(tracks, artists):
    # avg duration in minutes
    avg_duration = round(sum(t["duration_ms"] for t in tracks) / len(tracks) / 60000, 2)

    # explicit %
    explicit_count = sum(1 for t in tracks if t["explicit"])
    explicit_pct   = round(explicit_count / len(tracks) * 100, 1)

    # release year breakdown
    years = [t["release"][:4] for t in tracks if t["release"][:4].isdigit()]
    year_counts = Counter(years).most_common()

    # most repeated artist in top 20 tracks
    artist_counts = Counter(t["artist"] for t in tracks).most_common(5)

    # top genres from artists
    all_genres = []
    for a in artists:
        all_genres.extend(a["genres"])
    top_genres = Counter(all_genres).most_common(5)

    return {
        "avg_duration":   avg_duration,
        "explicit_pct":   explicit_pct,
        "year_counts":    year_counts,
        "artist_counts":  artist_counts,
        "top_genres":     top_genres
    }


def display(tracks, artists, stats):
    print(f"\n{'='*55}")
    print(f"  Your listening profile")
    print(f"{'='*55}")

    print(f"\n  Top 5 tracks (last 6 months):")
    for t in tracks[:5]:
        print(f"    • {t['artist']} - {t['name']}")

    print(f"\n  Top 5 artists:")
    for a in artists[:5]:
        genres = ", ".join(a["genres"][:3]) if a["genres"] else "no genre data"
        print(f"    • {a['name']}  [{genres}]")

    print(f"\n  Most repeated artists in your top tracks:")
    for name, count in stats["artist_counts"]:
        if count > 1:
            print(f"    • {name}  ×{count}")

    if stats["top_genres"]:
        print(f"\n  Top genres overall:")
        for genre, count in stats["top_genres"]:
            print(f"    • {genre}  ({count} artists)")

    print(f"\n  Release year breakdown:")
    for year, count in stats["year_counts"]:
        print(f"    • {year}  ×{count}")

    print(f"\n{'='*55}")
    print(f"  Avg track length : {stats['avg_duration']} min")
    print(f"  Explicit tracks  : {stats['explicit_pct']}%")
    print(f"{'='*55}\n")


def main():
    sp      = get_spotify_client()
    tracks  = get_top_tracks(sp)
    artists = get_top_artists(sp)
    stats   = analyze(tracks, artists)
    display(tracks, artists, stats)


if __name__ == "__main__":
    main()
