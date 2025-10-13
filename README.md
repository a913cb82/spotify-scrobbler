# Spotify Scrobbler

This script scrobbles your Spotify listening history to Last.fm. It reads your Spotify data from a JSON file and uses the Last.fm API to scrobble each track.

## How to Use

### 1. Request Your Spotify History

To get your Spotify listening history, you need to request it from Spotify. You can do this by following these steps:

1.  Go to your Spotify account settings page.
2.  In the "Privacy" section, select "Download your data".
3.  Follow the instructions to request your data. You will receive an email with a link to download your data in a few days.
4.  Download the data and look for a file named `Streaming_History_Audio_*.json`. This is the file you will use with this script.

**Note:** To get your full listening history, you may need to email Spotify support and request it.

### 2. Set Up Your Environment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/scrobble_spotify.git
    cd scrobble_spotify
    ```

2.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**
    Create a file named `.env` in the root of the project and add your Last.fm API credentials:
    ```
    LASTFM_API_KEY=your_api_key
    LASTFM_API_SECRET=your_api_secret
    LASTFM_USERNAME=your_username
    LASTFM_PASSWORD=your_password
    ```

### 3. Run the Script

Run the script with the path to your Spotify history file:

```bash
python scrobble.py path/to/your/Streaming_History_Audio_*.json
```

#### Arguments

*   `history_file`: Path to the Spotify history file.
*   `--dry-run`: Simulate scrobbling without sending data to Last.fm.
*   `--start-index`: Index to start scrobbling from.
*   `--max-scrobbles`: Maximum number of songs to scrobble. This is useful to avoid the daily Last.fm scrobble limit of around 3000 scrobbles.
