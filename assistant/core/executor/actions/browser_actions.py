import webbrowser
import urllib.parse
from assistant.decorators.actions_registry import register_action


@register_action(description="Search a query on YouTube")
def search_youtube(query: str):
    """Search a query on YouTube."""
    q = urllib.parse.quote_plus(query)
    url = f"https://www.youtube.com/results?search_query={q}"
    webbrowser.open(url)
    print(f"▶️ Searching YouTube for: {query}")


@register_action(description="Search a query on Google")
def search_google(query: str):
    """Search a query on Google."""
    q = urllib.parse.quote_plus(query)
    url = f"https://www.google.com/search?q={q}"
    webbrowser.open(url)
    print(f"🔎 Searching Google for: {query}")


@register_action(description="Search and open a song on Spotify Web")
def open_spotify_song(song: str):
    """Open a song on Spotify web."""
    q = urllib.parse.quote_plus(song)
    url = f"https://open.spotify.com/search/{q}"
    webbrowser.open(url)
    print(f"Searching Spotify for: {song}")


@register_action(description="Open Gmail in the default browser")
def open_gmail():
    """Open Gmail in the default browser."""
    webbrowser.open("https://mail.google.com/")
    print("📧 Opening Gmail")


@register_action(description="Open Google News in the default browser")
def read_news():
    """Open Google News."""
    webbrowser.open("https://news.google.com/")
    print("📰 Opening Google News")
