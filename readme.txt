
by:
Tarek Bdarny
id: 325347086
Mohamed abo rya
id: 213933138
This project can aggregate movie information from The movie database (tmdb) api.
You can select what you to aggregate, you can search by movie name,
or the top rated, up coming, now playing and popular movies.
in this project we used modular style to be more readable and more consestent.
You can also encrypt decrypt a file when downloaded and it saved to you'r computer,
When searching via movie name you can also download their poster image and backdrop image.
----------------------------------------------------------

explaining the code:
- movie-aggregator.py
options = {'p': helpers.getPupolarMovies,
           't': helpers.getTopRated,
           'n' : helpers.getNowPlaying,
           'u' : helpers.getUpComing,
           'f' : helpers.getFavorites
           }
We stored the function for the searching method in a dict to make it easy.

if type not in options.keys():
    helpers.getMovie(type, saveToFile, encrypt, addToFavorites)
else :
    options[type](saveToFile, encrypt)

if the user is searching for movie by name it will trigger the if statment because type(the movie name) is not in the dict,
if the user used on of the methods above it will trigger the else statment and will behave to the user commands
------------------------------------------------------------

-dataHelpers.py

def get_genres() => get all the genres in the api database
def get_genre_name(genre_id) get the speceifc genre by the id of the genre (api returns a genre id)

def formatData(result, single=False)=> it returns wanted data from the api response,
single => it determinate if we useing the function for the get movie function or to store it in the tinydb

def get_posters(result) => returns a dict of the url of the poster and backdrop images

def formatData2(result) => we use it to get all the data in the database 

-----------------------------------
- helpers.py
def getMovie(name, save, enc, fav):
this funciton is triggered when the user searching for movie by movie name, 

getPupolarMovies, getUpComing, getTopRated, getNowPlaying => Its the same consept just we pass diffrent url to the mian funciton fetch

def fetch(url,save, enc, file_name ) => make a request to the api, we use the helpers save_encrypted, write_to_file, formatData.
loop over the movies and saved them to the all_data variable

def save_encrypted(movie) => gets the data as formated and returns them as encrypted and orginazed

def write_to_file(file_name, formated_item, save=True) => if the user want to save we open the file and write the formated_item to it, if the user don't want to write we just print it

def saveFile(file_name, enc, movie) => if the user want to encrypt the data we get all data as encrypted and write to it.
after that if there the original name we remove it and, last we write to the file.
if the user don't want to encrypt we write the data as it is 

def download_image(image_path, file_name, enc) => we make a request to the api to download the image,
we right the image to a file as the movie we fetched.
If the user dont want to encrypt the image we saved it and exit out of the function,
otherwise we open the file that we maked earlier as rb to read the binary from the image,
then we encrypt the data using ceasar algo then we write to the enc file at last we remove the original file,
if the status code wasn't 200 we delete the file because its empty

----------------------------------------------------
 -decrypt.py

We ask the user for the file name and the type if its image or file that have text,
if the file dosen't exists we exit the program.
If the file dosen't start with enc_ (the file is not encrypted) we exit the program.
then we use normal decrypt for the type of the file