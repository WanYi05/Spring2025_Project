import requests
from typing import Dict

def get_genre_mapping(api_key: str, language: str = "zh-TW") -> Dict[int, str]:
    """
    從 TMDb API 抓取 genre 對照表，回傳一個 {genre_id: 類型名稱} 字典
    """
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language={language}"
    res = requests.get(url)
    
    if res.status_code != 200:
        raise Exception(f"無法取得 genre 對照表，HTTP 狀態碼：{res.status_code}")

    try:
        genres = res.json().get("genres", [])
    except Exception as e:
        raise Exception("API 回傳格式錯誤，無法解析 JSON") from e

    return {genre["id"]: genre["name"] for genre in genres}