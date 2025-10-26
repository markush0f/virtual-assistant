import webbrowser
import urllib.parse


def search_youtube(query: str):
    """Search a query on YouTube."""
    q = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={q}"
    webbrowser.open(url)
    print(f"▶️ Searching YouTube for: {query}")


def search_google(query: str):
    """Search a query on Google."""
    q = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={q}"
    webbrowser.open(url)
    print(f"🔎 Searching Google for: {query}")


def open_spotify_song(song: str):
    """Open a song on Spotify web."""
    q = urllib.parse.quote_plus(song)
    url = f"https://open.spotify.com/search/{q}"
    webbrowser.open(url)
    print(f"🎵 Searching Spotify for: {song}")


def open_gmail():
    """Open Gmail in the default browser."""
    webbrowser.open("https://mail.google.com/")
    print("📧 Opening Gmail")


def read_news():
    """Open Google News."""
    webbrowser.open("https://news.google.com/")
    print("📰 Opening Google News")
