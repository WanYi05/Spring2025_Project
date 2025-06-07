import os
import pandas as pd

from src.genre_utils import get_genre_mapping
from src.process_data import clean_movie_data, convert_genre_ids_to_names, add_context
from src.tmdb_api import get_movies_by_genre
from src.recommender import recommend_by_context


# 記得放你自己的 API Key
API_KEY = "8c6bf4281a91a56e3333a0affe66f5a0"

# ✅ Step 2: 抓 genre 對照表
genre_map = get_genre_mapping(API_KEY)

if not genre_map:
    print("⚠️ 無法取得 genre 對照表，請檢查 API Key 是否正確。")
    exit()

# print("🎬 類型對照表：")
# print(genre_map)

# ✅ Step 3: 確保資料夾存在
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# ✅ Step 4: 檢查喜劇電影資料是否已存在
csv_path = "data/raw/comedy_movies.csv"

if not os.path.exists(csv_path):
    print("🔍 資料不存在，從 TMDb 抓取中...")
    movies = get_movies_by_genre(genre_id=35, pages=2)
    df_raw = pd.DataFrame(movies)
    df_raw.to_csv(csv_path, index=False, encoding="utf-8-sig")
    print(f"✅ 資料已抓取，共 {len(df_raw)} 筆")
# else:
#     print("📂 已找到本地資料，不重新抓取。")  # ← 已隱藏

# ✅ Step 5: 資料處理
df = clean_movie_data(csv_path)
df = convert_genre_ids_to_names(df, genre_map)
df = add_context(df)

# ⏺️ 儲存處理後的資料（供除錯或分析）
df.to_csv("data/processed/comedy_processed.csv", index=False, encoding="utf-8-sig")

# ✅ Step 6: 使用者輸入情境
user_input = input("請輸入情境（例如：輕鬆）：")

# ✅ Step 7: 進行推薦
results = recommend_by_context(user_input, df)

# ✅ Step 8: 顯示推薦結果
print("\n📽️ 推薦片單：")
if results.empty:
    print("😢 沒有符合的結果。")
else:
    for _, row in results.iterrows():
        print(f"🎞️ {row['title']} - ⭐ {row['vote_average']}")
        if not pd.isna(row["overview"]):
            print(f"簡介：{row['overview']}\n")
        else:
            print("簡介：這部電影沒有提供簡介。\n")