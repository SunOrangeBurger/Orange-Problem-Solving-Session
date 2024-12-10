import csv
import tkinter as tk
from tkinter import ttk, messagebox

def read_csv(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data
#print(read_movies('movie_dataset.csv'))
#for checks
def get_genre_columns(file_path):
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        #the genre header starts from the 4th column(third index)
        genre_columns = headers[3:]
    return genre_columns

#print(get_genre_columns('movie_dataset.csv'))
#for checks
def create_widgets(root, genres):
    # Instruction label for the user
    instruction_label = tk.Label(root, text="Select your favourite genres", font=("Bold", 16), fg="red")
    instruction_label.pack(padx=10, pady=(10, 5))
    
    #frame
    checkbox_frame = tk.LabelFrame(root, text="Select Genres")
    checkbox_frame.pack(padx=10, pady=10, fill='x')
    
    genre_vars = {}
    for genre in genres:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(checkbox_frame, text=genre, variable=var)
        chk.pack(side='left', padx=5, pady=5)
        genre_vars[genre] = var
    
    #Frame 
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    recommend_btn = tk.Button(button_frame, text="Recommend", command=lambda: recommend(genre_vars, tree, genres))
    recommend_btn.pack(side='left', padx=5)

    clear_btn = tk.Button(button_frame, text="Clear", command=lambda: clear_selection(genre_vars, tree))
    clear_btn.pack(side='left', padx=5)

    #implemented a treeview using ttk
    tree = ttk.Treeview(root, columns=('Title', 'Release Year', 'Rating', 'Genres'), show='headings')
    tree.heading('Title', text='Title')
    tree.heading('Release Year', text='Release Year')
    tree.heading('Rating', text='Rating')
    tree.heading('Genres', text='Genres')
    tree.pack(padx=10, pady=10, fill='both', expand=True)

    #highlight top pick
    tree.tag_configure('top_pick', background='lightgreen')

    return tree

def recommend(genre_vars, tree, genres):
    selected_genres = [genre for genre, var in genre_vars.items() if var.get()]
    
    if not selected_genres:
        #if no genres are selected, prepare to show top 5 movies
        filtered_movies = []
    else:
        filtered_movies = []
        for movie in data:
            movie_genres = [genre for genre in genres if movie[genre] == '0']
            if all(genre in movie_genres for genre in selected_genres):
                filtered_movies.append({
                    'Title': movie['Title'],
                    'Release Year': movie['Release Year'],
                    'Rating': movie['Rating'],
                    'Genres': ', '.join(movie_genres)
                })

    if not filtered_movies:
        #show top 5 movies based on rating
        top_movies = sorted(
            [
                {
                    'Title': movie['Title'],
                    'Release Year': movie['Release Year'],
                    'Rating': movie['Rating'],
                    'Genres': ', '.join([genre for genre in genres if movie[genre] == '0'])
                }
                for movie in data
            ],
            key=lambda x: float(x['Rating']),
            reverse=True
        )[:5]
        display_movies(tree, top_movies, top_pick=top_movies[0] if top_movies else None)
    else:
        #Sort
        sorted_movies = sorted(filtered_movies, key=lambda x: float(x['Rating']), reverse=True)
        display_movies(tree, sorted_movies, top_pick=sorted_movies[0])

def display_movies(tree, movies, top_pick=None):
    for item in tree.get_children():
        tree.delete(item)

    for movie in movies:
        tree.insert('', 'end', values=(movie['Title'], movie['Release Year'], movie['Rating'], movie['Genres']))

    #highlight
    if top_pick:
        for item in tree.get_children():
            if tree.item(item)['values'][0] == top_pick['Title']:
                tree.item(item, tags=('top_pick',))
                break

def clear_selection(genre_vars, tree):
    #resets alll button values to falseererere
    for var in genre_vars.values():
        var.set(False)

    for item in tree.get_children():
        tree.delete(item)

def main():
    global data
    file_path = 'movie_dataset.csv'
    data = read_csv(file_path)
    genres = get_genre_columns(file_path)
    root = tk.Tk()
    root.title("Movie Recommendations")
    tree = create_widgets(root, genres)
    root.mainloop()

if __name__ == "__main__":
    main()
