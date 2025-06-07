import pandas as pd
import ast

# Step 1: 清洗原始欄位（讀取 title / overview / vote / genre_ids）
def clean_movie_data(filepath):
    df = pd.read_csv(filepath)
    return df[["title", "overview", "vote_average", "genre_ids"]]

# Step 2: 將 genre_ids 轉成 genre_names
def convert_genre_ids_to_names(df, genre_map):
    def map_genres(genre_ids):
        ids = ast.literal_eval(genre_ids) if isinstance(genre_ids, str) else genre_ids
        return [genre_map.get(i, "未知") for i in ids]

    df["genre_names"] = df["genre_ids"].apply(map_genres)
    return df

# Step 3: 加入 context 欄位
def add_context(df):
    context_keywords = {
        "療癒": ["家庭", "音樂", "愛情", "動畫"],
        "輕鬆": ["喜劇", "動畫", "家庭", "冒險"],
        "懸疑": ["驚悚", "犯罪"]
    }

    df["context"] = "其他"

    for context, keywords in context_keywords.items():
        df.loc[
            df["genre_names"].apply(lambda genres: any(k in genres for k in keywords)),
            "context"
        ] = context

    # print(df[["title", "genre_names", "context"]].head(10))  # debug 用
    return df
