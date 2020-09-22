import requests
import json

def get_movies_from_tastedive(query):
    param_dict = {}
    param_dict['q'] = query
    param_dict['type'] = 'movies'
    param_dict['limit'] = 5
    base_url = "https://tastedive.com/api/similar"
    result = requests.get(base_url, params = param_dict)
    return result.json()

def extract_movie_titles(d):
    lst = []
    for title in d["Similar"]["Results"]:
        lst.append(title['Name'])
    return lst

def get_related_titles(lst):
    rlst = []
    for movie in lst:
        for m in extract_movie_titles(get_movies_from_tastedive(movie)):
            if m in rlst:
                continue
            else:
                rlst.append(m)
    return rlst   

def get_movie_data(title):
    base_url = "http://www.omdbapi.com/"
    param_dict = {}
    param_dict["t"] = title
    param_dict["r"] = "json"
    result = requests.get(base_url, params = param_dict)
    info = result.json()
    return info

def get_movie_rating(d):
    r_lst = d["Ratings"]
    rt_rating = 0
    for s in r_lst:
        if s["Source"] == "Rotten Tomatoes":
            rating = s["Value"]
            rating = rating[:-1]
            rt_rating = int(rating)
    return rt_rating

def rotten_tomato_rating(title):
    d = get_movie_data(title)
    rating = get_movie_rating(d)
    return (rating,title)

def get_sorted_recommendations(lst):
    m_lst = get_related_titles(lst)
    sort_lst = []
    for movie in m_lst:
        t = rotten_tomato_rating(movie)
        sort_lst.append(t)
    new_list = list(sorted(sort_lst, reverse = True))
    sorted_list = []
    for m in new_list:
        sorted_list.append(m[1])
    return sorted_list
        
        
get_sorted_recommendations(["Black Panther", "The Alchemist"])