from requests import get
from pprint import pprint
import dataHelpers
import os
from PIL import Image
from io import BytesIO

from tinydb import TinyDB, Query

db = TinyDB('./db.json')
Movies = Query()
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/original'
# header includes the access token
headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJlZWQ1ZjM5ZGFiYmM4NzhlOThlMTk2NmJkMTgxNzY3YiIsIm5iZiI6MTcyMjg5NDMxNi45NTIzOTgsInN1YiI6IjY2YWZlMmRiYzZkOTllOWViZDNhMGM0NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.s6C5W6o_r8ruWqkTdMDR62XLwEg5yJDwyrh3ricembU"
}
ceasar_enc = lambda chunk ,key=3 : chr(ord(chunk) + key % 26)  
ceasar_enc_bytes = lambda chunk ,key=3 : bytes([(ord(chunk) +key)%256])

# vv
def getMovie(name, save, enc, fav):
    url = f'https://api.themoviedb.org/3/search/movie?query={name}'
    res = get(url, headers=headers).json()
    movie = dataHelpers.formatData(res["results"][0])
    want_to_remove = input("You want to remove the movie from favorites? [y/n]")
    store_images=  input("Do you want to download poster and backrop images [y/n]")
    if store_images == 'y':
        paths = dataHelpers.get_posters(res['results'][0])
        download_image(paths["p"], f'{name}_poster.png', enc)
        download_image(paths["b"], f'{name}_backdrop.png', enc)
    type = "enc_" if enc == True else ""
    file_name = type + name+".txt"
    if not save : # if the user dont want to save 
        print(movie)
    else:
        saveFile(file_name,enc, movie)
        #saving to file
    # if checking
    if fav == True and want_to_remove == 'y':
        print("You can't add to favorites and remove it at the same time.")
        exit()
    elif fav == False and want_to_remove == 'y':
        #remove logic > check if exists
        db.remove(Movies.title == name)
        print("deleeted")
        exit()
    elif fav == True and want_to_remove == 'n':  
        movie = dataHelpers.formatData(res["results"][0], True)
        db.insert(movie)
    


# vv
def getPupolarMovies(save, enc):
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"
    fetch(url, save, enc , "Popualar Movies")
    


def getFavorites(save, enc):
    if save :
        f = open("favories.txt", "w+")
        for item in db:
            formated_item = dataHelpers.formatData2(item)
            for f_item in formated_item:
                f.write(f_item + ' : ' + str(formated_item[f_item]))
                f.write('\n')
            
        f.close()

    else:
        print(db.all())
    
    

def getUpComing(save, enc):
    url = "https://api.themoviedb.org/3/movie/upcoming?language=en-US&page=1"
    fetch(url, save, enc, "Up Coming Movies")



def getTopRated(save, enc):
    url = "https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1"
    fetch(url, save, enc, "Top Rated Movies")

# vv
def getNowPlaying(save, enc):
    url = "https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1"
    fetch(url, save, enc, "Now Playing Movies")
    
def fetch(url,save, enc, file_name ):
    if enc and not save:
        print("You can't read encrypted values")
        print("You must save to a file then decrypt it")
        exit()

    res = get(url, headers=headers)
    data = res.json();
    movies = data["results"]
    type = "enc_"if enc else "" # what the name for the file
    all_data = "" # all the data from the request
        
    count =0 # counter to sent the message in the prosess of fetching the data
    for movie in movies:
        if count == 7:
            print("Retreving data") # to send the message in the prosecc of fetching the data 
        count+=1
        formated_item = str(count) + ') ' + dataHelpers.formatData(movie)
        all_data += save_encrypted(formated_item) if enc else formated_item + '\n'
    write_to_file(type + file_name, all_data,save)
    print("succsessfully")


def download_image(image_path, file_name, enc):
    image_url = f"{IMAGE_BASE_URL}{image_path}"
    img_response = get(image_url)
    f = open(file_name, 'wb+')
    f.write(img_response.content)
    if img_response.status_code == 200 and not enc:
        print(f"Image saved as {file_name}")
        return
    elif img_response.status_code == 200 and enc:
        wanted_file = open(file_name, "rb")
        chunk = wanted_file.read(1) 
        file_arr = bytearray()
        while chunk:
            file_arr += ceasar_enc_bytes(chunk)
            chunk = wanted_file.read(1)
        res_file = open('enc_'+file_name, 'wb+')
        res_file.write(file_arr)
        # os.chmod(f'/enc_{file_name}')
        os.remove(f'{file_name}')
    else:
        os.remove(file_name)
        print(f"Failed to download image: {img_response.status_code}")

def save_encrypted(movie):
    all_data = ""
    for ch in movie:
        if ch == ' ':
            all_data += " "
        elif ch == '\n':
            all_data += '\n'
        else:
            all_data += ceasar_enc(ch)
    return all_data

def saveFile(file_name, enc, movie): 
    
    file = open(file_name, 'w+')
    if enc:
        data = save_encrypted(movie)
        original_name = file_name.replace('enc_', '')
        if os.path.exists(original_name):
            os.remove(original_name)
        file.write(data)
        print(f'File successfully saved {"and encrypted" if enc == True else ""}')
    else:
        file.write(movie)

def write_to_file(file_name, formated_item, save=True):
    if save:
        f = open(f'{file_name}.txt', 'w+')
        f.write(formated_item)
        f.write('\n')
        f.close()
    else:
        print(formated_item)
    

