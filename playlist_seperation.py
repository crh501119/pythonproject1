import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

def main():
    # 禁用 OAuthlib 的 HTTPS 檢查
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # 讀取憑證文件
    client_secrets_file = r"C:\Users\Howard\Downloads\client_secret_723556654345-5rskeng3o2eiic65jvinpcnv2ssgvcd6.apps.googleusercontent.com.json"

    # 獲取認證並建立 API 客戶端
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)

    # 獲取原始播放清單中的視頻
    def get_playlist_items(playlist_id, max_results=10):
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=max_results
        )
        response = request.execute()
        return response.get('items', [])

    # 創建新的播放清單
    def create_playlist(title, description=""):
        request = youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": "private"
                }
            }
        )
        response = request.execute()
        return response['id']

    # 將視頻添加到播放清單
    def add_video_to_playlist(playlist_id, video_id):
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        request.execute()

    def remove_video_from_playlist(playlist_item_id):
        request = youtube.playlistItems().delete(id=playlist_item_id)
        request.execute()

    original_playlist_id = 'PLvJCsOI1kVLhbIA2yieyg6yUN3aoROEEM'
    items = get_playlist_items(original_playlist_id)

    new_playlist_id = create_playlist("New Playlist Title")

    for item in items[:10]:  # 假設我們只取前10首歌曲作為示例
        video_id = item['snippet']['resourceId']['videoId']
        add_video_to_playlist(new_playlist_id, video_id)
        remove_video_from_playlist(item['id'])

    print(f"Created new playlist with ID: {new_playlist_id}")

if __name__ == "__main__":
    main()
