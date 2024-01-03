from googleapiclient.discovery import build
import pandas as pd

# 你的API鑰匙和播放清單ID
api_key = 'AIzaSyArwzeFaBqTtoB9NhNXfGnOSmAwgv220qc'
playlist_id = 'PLvJCsOI1kVLhbIA2yieyg6yUN3aoROEEM'

youtube = build('youtube', 'v3', developerKey=api_key)


def get_playlist_videos(playlist_id):
    """
    獲取YouTube播放清單中的視頻資訊
    """
    videos = []
    next_page_token = None

    while True:
        pl_request = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )

        pl_response = pl_request.execute()

        video_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

        # 獲取視頻詳細資訊
        videos_request = youtube.videos().list(
            part="snippet",
            id=','.join(video_ids)
        )

        videos_response = videos_request.execute()

        for i, item in enumerate(videos_response['items'], start=1):
            video_title = item['snippet']['title']
            video_url = f"https://www.youtube.com/watch?v={item['id']}"

            videos.append([i, video_title, video_url])

        next_page_token = pl_response.get('nextPageToken')

        if not next_page_token:
            break

    return videos


# 獲取播放清單中的視頻
playlist_videos = get_playlist_videos(playlist_id)

# 創建DataFrame
df = pd.DataFrame(playlist_videos, columns=['編號', '名稱', 'URL'])

# 導出為Excel
excel_filename = 'youtube_playlist.xlsx'
df.to_excel(excel_filename, index=False)

print(f"播放清單數據已導出到 {excel_filename}")
