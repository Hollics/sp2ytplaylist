from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


DEVELOPER_KEY = "DEV_KEY"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search():
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)
    return youtube

 # Call the search.list method to retrieve results matching the specified
 # query term.

youtube = youtube_search()

def search_musics(youtube, music_name):
    search_response = youtube.search().list(
    q=music_name,
    part="id,snippet",
    maxResults=5
    ).execute()
    return search_response


  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
def get_music_id(search_response):
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            music_id = search_result["id"]["videoId"]
            break
    return music_id


if __name__ == "__main__":
  print('You should run spotify_transfer.py')
else:
    print('youtube_search.py')
