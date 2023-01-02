from tkinter import *
import pandas as pd
from tkinter import ttk
from matplotlib import pyplot as plt
from PIL import Image, ImageTk
from urllib.request import urlopen

win = Tk()
win.title('Movie Recommender System')

#Set the geometry of tkinter frame
win.geometry("900x900")
win.configure(bg="#008080")

# image = Image.open('images/Bg.png')
# image = image.resize((1530, 800))
# image.save('images/resized_Bg.png')

# canvas = Canvas(win, width=1530, height=800)
# canvas.pack()
# image_id = canvas.create_image(250, 250, image=image)
# canvas.tag_lower(image_id)
# img = PhotoImage(file='images/resized_Bg.png')
# label = Label(win, image = img)
# label.pack()

#reading the CSVs
data_csv = pd.read_csv("Dataset/movies_metadata.csv",low_memory=False)

Movies = data_csv['original_title']
Movie_Image_List = data_csv['poster_path']
movie_ids = data_csv['imdb_id']

#creating poster_urls
import requests

CONFIG_PATTERN = 'http://api.themoviedb.org/3/configuration?api_key={key}'
KEY = '3e982460412cce495589b8ef26282d84'

url = CONFIG_PATTERN.format(key=KEY)
r = requests.get(url)
config = r.json()

poster_urls = []

def poster_func(movie_id):
    base_url = config['images']['base_url']
    sizes = config['images']['poster_sizes']
    # def size_str_to_int(x):
    #     return float("inf") if x == 'original' else int(x[1:])
    # max_size = max(sizes, key=size_str_to_int)
    IMG_PATTERN = 'http://api.themoviedb.org/3/movie/{imdbid}/images?api_key={key}'
    r = requests.get(IMG_PATTERN.format(key=KEY,imdbid=movie_id))
    api_response = r.json()

    rel_path = api_response['posters'][0]['file_path']
    poster_url = base_url + 'w92' + rel_path
    
    poster_urls.append(poster_url)

exception_list = []
for id in movie_ids[:100]:
    try:
        poster_func(id)
    except:
        exception_list.append(id)

def update(Movies):
    my_list.delete(0, END)
    for movie in Movies:
        my_list.insert(END, movie)

def fillout(e):
    my_entry.delete(0,END)
    my_entry.insert(0,my_list.get(ACTIVE))

def check(e):
    typed = my_entry.get()

    if typed == '':
        data = Movies
    else: 
        data = []
        for movie in Movies:
            if typed.lower() in movie.lower():
                data.append(movie)
    update(data)

#creating Frame
frame1 = Frame(win)

my_label = Label(frame1,text="Search For Movie...", font=("Helvetica", 11), fg = "#81cdc6", bg = "#008080")
my_label.pack(pady=20)

my_entry = Entry(frame1,font=("Helvetica", 10),bg=("#81cdc6"),width=50)
my_entry.pack()

my_list = Listbox(frame1,font=("Helvetica", 10),bg=("#81cdc6"),width=50)
my_list.pack()

frame1.pack(side=LEFT,expand=True,fill=BOTH)

# Recommendation System Types
options = ['Basic Recommender System', 'Content Based Recommender System', 'Collaborative Filtering Recommender System']
combo = ttk.Combobox(frame1, values=options)
combo.pack()

# Recommendation Types
options = ['IMDB Rating', 'Genre Based', 'Popularity']
combo = ttk.Combobox(frame1, values=options)
combo.pack()

#showing posters
frame2 = Frame(win)

for i in range(5):
    image_url = poster_urls[i]
    u = urlopen(image_url)
    raw_data = u.read()
    u.close()

    photo = ImageTk.PhotoImage(data=raw_data)
    label = Label(frame2, image=photo)
    label.image = photo
    label.pack()
    movie_image = PhotoImage()
    
frame2.pack(side=LEFT,expand=True,fill=BOTH)

#update
update(Movies)
my_list.bind("<<ListboxSelect>>", fillout)
my_entry.bind("<KeyRelease>", check)

win.mainloop()