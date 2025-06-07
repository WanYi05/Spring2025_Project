import requests

API_KEY = "8c6bf4281a91a56e3333a0affe66f5a0"  

def get_movies_by_genre(genre_id=35, pages=1):
    """
    根據 TMDb 類型 ID 抓取電影清單
    預設 genre_id=35（喜劇）
    """
    all_movies = []
    for page in range(1, pages + 1):
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&with_genres={genre_id}&page={page}&language=zh-TW"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            all_movies.extend(data['results'])
        else:
            print("錯誤：", response.status_code)
    return all_movies
