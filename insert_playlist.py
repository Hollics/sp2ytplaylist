import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube",
          "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtubepartner"]

def setup_connection():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    return youtube

def send_to_ytplaylist(youtube, playlist_id, music_id_list):
    for i in range(len(music_id_list)):
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": music_id_list[i]
                }
              }
            }
        )
        response = request.execute()
        print('Music has been added!')
    print("All musics has been added!!")

if __name__ == "__main__":
    print('You should run spotify_transfer.py')
else:
    print('insert_playlist.py')
    youtube = setup_connection()
