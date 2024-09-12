
import requests
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZWQ1ZjM5ZGFiYmM4NzhlOThlMTk2NmJkMTgxNzY3YiIsIm5iZiI6MTcyMjg5NDMxNi45NTIzOTgsInN1YiI6IjY2YWZlMmRiYzZkOTllOWViZDNhMGM0NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.s6C5W6o_r8ruWqkTdMDR62XLwEg5yJDwyrh3ricembU"
}

def get_genres():
    """Fetches the list of genres from TMDb."""
    url = "https://api.themoviedb.org/3/genre/movie/list"
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()['genres']

def get_genre_name(genre_id):
    """Finds the genre name from the genre ID using TMDb API."""
    genres = get_genres()
    for genre in genres:
        if genre['id'] == genre_id:
            return genre['name']
    return None

def formatData(result, single=False):
    """ original_title, overview, vote_count, vote_average, release_date,adult, genres_id """
    for_adults = 'yes' if result['adult'] == 'true' else 'no'
    title = result['original_title']
    overview = result['overview']
    release_date = result['release_date']
    vote_average = result['vote_average']
    vote_count = result['vote_count']
    genres_names = ""
    for genre in result['genre_ids'] :
        genres_names += (get_genre_name(genre) + ', ')
    if not single:
        return f'title: {title} \n for adults: {for_adults} \n release date: {release_date} \n overview: {overview} \n genres: {genres_names} \n average: {vote_average} \n votes: {vote_count} \n'
    else:
        return {'title' : title, 'for adults' : for_adults, 'release date' : release_date, 'overview' : overview,'genres' : genres_names,'average' : vote_average, 'votes' : vote_count,
             }

def get_posters(result):
    poster_path = result['poster_path']
    backdrop_path = result['backdrop_path']
    return {"p" : poster_path, "b" : backdrop_path}

def formatData2(result):
    """ original_title, overview, vote_count, vote_average, release_date,adult, genres_id """
    for_adults = 'yes' if result['for adults'] == 'true' else 'no'
    title = result['title']
    overview = result['overview']
    release_date = result['release date']
    vote_average = result['average']
    vote_count = result['votes']
    genres_names = ""
    
    return {'title' : title, 'for adults' : for_adults, 'release date' : release_date, 'overview' : overview,'average' : vote_average, 'votes' : vote_count,
             }
  

