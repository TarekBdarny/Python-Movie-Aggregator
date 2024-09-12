import helpers
import argparse


parser = argparse.ArgumentParser(
                    prog='Movie Aggregator',
                    description=
                    'This tool aggregate movie details of the movie you search you also can store the data in a file, with option to encrypt/decrypt a file, add the movie to you favorites/watch list,remove from favorites/watch list, see all movies categories [1-5]  '
                    )
                    
parser.add_argument('-t' ,
'--type' ,
help="What you looking to aggregate by entring the movie name or the follwing options. \n p-[popular] \n t-[top rated] \n n-[now playing] \n u-[up coming] ",
required=True
)

parser.add_argument('-s' ,
'--save' ,
help='You can save the information to a file [y/n].',
required=True
)

parser.add_argument('-e' ,
'--encrypt' ,
help='You can encrypt the information after aggregation [y/n]'
)

parser.add_argument('-f' ,
'--favorites' ,
help='You can add a certian movie to favorites. [y/n]'
)





args = parser.parse_args()
# getting the values that the user typed 
type = args.type
addToFavorites = True if args.favorites == 'y' else False
saveToFile = True if args.save == 'y' else False
encrypt = True if args.encrypt == 'y' else False

options = {'p': helpers.getPupolarMovies,
           't': helpers.getTopRated,
           'n' : helpers.getNowPlaying,
           'u' : helpers.getUpComing,
           'f' : helpers.getFavorites
           }
if addToFavorites and type in options.keys():
    print("You can't add a list to your favorites")
    print("You need to enter a movie name to add it to you'r favorites")
    exit()


if type not in options.keys():
    helpers.getMovie(type, saveToFile, encrypt, addToFavorites)
else :
    options[type](saveToFile, encrypt)



