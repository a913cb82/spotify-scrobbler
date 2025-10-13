
import json
import pylast
import datetime
import hashlib
import os
import argparse
import time
from dotenv import load_dotenv

load_dotenv()

def main():
    """Scrobble Spotify history to Last.fm."""
    parser = argparse.ArgumentParser(description="Scrobble Spotify history to Last.fm.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate scrobbling without sending data to Last.fm.")
    parser.add_argument("--start-index", type=int, default=0, help="Index to start scrobbling from.")
    parser.add_argument("--max-scrobbles", type=int, default=None, help="Maximum number of songs to scrobble.")
    parser.add_argument("history_file", help="Path to the Spotify history file.")
    args = parser.parse_args()

    api_key = os.getenv("LASTFM_API_KEY")
    api_secret = os.getenv("LASTFM_API_SECRET")
    username = os.getenv("LASTFM_USERNAME")
    password = os.getenv("LASTFM_PASSWORD")

    if not all([api_key, api_secret, username, password]):
        print("Error: Please set LASTFM_API_KEY, LASTFM_API_SECRET, LASTFM_USERNAME, and LASTFM_PASSWORD in a .env file.")
        return

    password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()

    try:
        network = pylast.LastFMNetwork(
            api_key=api_key,
            api_secret=api_secret,
            username=username,
            password_hash=password_hash,
        )
    except pylast.WSError as e:
        print(f"Error connecting to Last.fm: {e}")
        return

    try:
        with open(args.history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        print(f"Error: {args.history_file} not found.")
        return
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the history file.")
        return

    scrobbled_count = 0
    # Start scrobbling from 1 hour ago
    scrobble_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)

    for i, item in enumerate(history[args.start_index:]):
        if args.max_scrobbles and scrobbled_count >= args.max_scrobbles:
            print(f"Reached max scrobbles limit of {args.max_scrobbles}.")
            break

        try:
            if item['ms_played'] < 30000:
                print(f"Skipping song at index {args.start_index + i} due to listen time being under 30 seconds.")
                continue

            artist = item['master_metadata_album_artist_name']
            track = item['master_metadata_track_name']
            
            unix_timestamp = int(scrobble_time.timestamp()) + scrobbled_count

            if artist and track:
                log_message = f"Song ID (index): {args.start_index + i} | Scrobbling: {artist} - {track}"
                if args.dry_run:
                    print(f"[DRY RUN] {log_message}")
                else:
                    print(log_message)
                    try:
                        network.scrobble(
                            artist=artist,
                            title=track,
                            timestamp=unix_timestamp
                        )
                    except pylast.WSError as e:
                        print(f"Error scrobbling {artist} - {track}: {e}")
                    except Exception as e:
                        print(f"An unexpected error occurred while scrobbling: {e}")
                scrobbled_count += 1
                time.sleep(0.5)  # Add a delay to avoid rate limiting

        except KeyError:
            with open("debug.log", "a", encoding="utf-8") as debug_file:
                debug_file.write(f"KeyError for item at index {args.start_index + i}: {json.dumps(item)}\n")
            print(f"Skipping item at index {args.start_index + i} due to missing data. See debug.log for details.")
        except Exception as e:
            print(f"An error occurred at index {args.start_index + i}: {e}")

if __name__ == "__main__":
    main()
