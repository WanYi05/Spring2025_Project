import pandas as pd

def recommend_by_context(context, df, top_n=5):
    """
    根據使用者輸入的情境（context），推薦前 top_n 部電影
    """
    # 過濾 context 欄位
    matched = df[df["context"] == context]

    # 依 vote_average 排序取前 top_n 名
    top_movies = matched.sort_values(by="vote_average", ascending=False).head(top_n)

    return top_movies