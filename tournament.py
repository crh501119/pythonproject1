import pandas as pd

# 載入播放清單數據
def load_playlist(file_path):
    return pd.read_excel(file_path)

# 創建初始淘汰賽配對
def create_initial_matchups(df):
    shuffled_df = df.sample(frac=1).reset_index(drop=True)
    matchups = []
    for i in range(0, len(shuffled_df), 2):
        if i + 1 < len(shuffled_df):
            matchups.append((shuffled_df.iloc[i]['名稱'], shuffled_df.iloc[i+1]['名稱']))
    return matchups

# 管理淘汰賽
def manage_tournament(matchups):
    results = []
    for round_number, matchup in enumerate(matchups, start=1):
        print(f"第 {round_number} 場比賽: {matchup[0]} vs {matchup[1]}")
        winner_index = int(input("請輸入勝者 (0代表前者, 1代表後者): "))
        winner = matchup[winner_index]
        results.append(winner)
    return results

# 主程序
def main():
    file_path = 'youtube_playlist.xlsx'  # 修改為實際的文件路徑
    playlist_df = load_playlist(file_path)
    matchups = create_initial_matchups(playlist_df)
    results = manage_tournament(matchups)
    print("淘汰賽結果：")
    for winner in results:
        print(winner)

# 執行主程序
if __name__ == "__main__":
    main()
