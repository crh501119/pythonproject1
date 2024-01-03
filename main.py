import webview
from googleapiclient.discovery import build
from create_html_for_songs import *
import pandas as pd

# 您的API密鑰
api_key = 'AIzaSyArwzeFaBqTtoB9NhNXfGnOSmAwgv220qc'

youtube = build('youtube', 'v3', developerKey=api_key)
def get_playlist_items(playlist_id):
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=1000  # 您可以根據需要調整這個值
    )
    response = request.execute()

    items = []
    for item in response['items']:
        title = item['snippet']['title']
        video_id = item['snippet']['resourceId']['videoId']
        items.append({'title': title, 'video_id': video_id})

    return items


class SongComparer:
    def __init__(self, songs):
        self.songs = songs
        self.temp_array = [None] * len(songs)  # 临时数组用于合并
        self.merged_index = 0
        self.left_index = 0  # 当前归并排序的左边界
        self.right_index = 0  # 当前归并排序的右边界

    def start_merge_sort(self):
        self.merge_sort(0, len(self.songs))

    def merge_sort(self, left, right):
        if right - left > 1:
            mid = (left + right) // 2
            self.merge_sort(left, mid)
            self.merge_sort(mid, right)
            self.merge(left, mid, right)

    def merge(self, left, mid, right):
        i = left
        j = mid
        k = left

        # 设置归并排序当前处理的边界
        self.left_index = left
        self.right_index = right
        
        while i < mid and j < right:
            # 此处等待用户的选择
            self.update_view(i, j)
            break

    def update_view(self, left_song_index, right_song_index):
        # 更新界面以显示当前比较的两首歌曲
        html_content = create_html_for_songs(self.songs[left_song_index], self.songs[right_song_index])
        webview.windows[0].load_html(html_content)

    def choose(self, win_index):
        # 根据用户选择更新临时数组
        if win_index == 0:
            self.temp_array[self.merged_index] = self.songs[self.left_index]
            self.left_index += 1
        else:
            self.temp_array[self.merged_index] = self.songs[self.right_index]
            self.right_index += 1
        self.merged_index += 1

        # 检查是否需要从左侧或右侧数组中取下一个元素
        if self.left_index < self.mid and self.right_index < self.right:
            self.update_view(self.left_index, self.right_index)
        else:
            # 将剩余的元素复制到临时数组中
            while self.left_index < self.mid:
                self.temp_array[self.merged_index] = self.songs[self.left_index]
                self.left_index += 1
                self.merged_index += 1

            while self.right_index < self.right:
                self.temp_array[self.merged_index] = self.songs[self.right_index]
                self.right_index += 1
                self.merged_index += 1

            # 将排序后的元素复制回原数组
            for i in range(self.left, self.right):
                self.songs[i] = self.temp_array[i]

            # 继续归并排序的下一个部分，或者如果完成，则显示结果
            if self.is_sorting_done():
                self.show_results(self)
            else:
                self.continue_merge_sort()

    def is_sorting_done(self):
        # 所有的歌曲都已经排序完毕，如果没有更多的子数组需要合并
        return len(self.waiting_list) == 1 and len(self.waiting_list[0]) == len(self.songs)

    def continue_merge_sort(self):
        if len(self.waiting_list) > 1:
            self.left_array = self.waiting_list.pop()
            self.right_array = self.waiting_list.pop()
            self.merge()
        else:
            # 如果等待列表为空，表示所有的子数组都已经合并完毕
            self.show_results()

    def show_results(self):
        # 展示排序结果
        for index, song in enumerate(self.songs):
            print(f"{index + 1}: {song['title']} - {song['url']}")

        # 创建并保存表格
        import pandas as pd
        data = {
            "名次": [i + 1 for i in range(len(self.songs))],
            "歌名": [song['title'] for song in self.songs],
            "URL": [song['url'] for song in self.songs]
        }
        df = pd.DataFrame(data)
        df.to_excel("排序结果.xlsx", index=False)


def start_gui(songs):
    comparer = SongComparer(songs)
    initial_html = create_html_for_songs(songs[0], songs[1])  # 第一首和最后一首歌曲
    webview.create_window("歌曲比较", html=initial_html, js_api=comparer)
    webview.start()

playlist_id = 'PLvJCsOI1kVLgcvvhi1-B4ln1DeGMB3cT0'
songs = get_playlist_items(playlist_id)
start_gui(songs)
