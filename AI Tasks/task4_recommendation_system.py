import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import ttk
data = {
    'title': [
        "I don't love you anymore", 'The Scarlet Letter', "Gulliver's Travels", 'Alice in Wonderland',
        'Uncharted', 'Rampage', 'The Godfather', 'The Dark Knight',
        'iPhone 13', 'Samsung Galaxy S21', 'OnePlus 9', 'Redmi Note 9'
    ],
    'category': [
        'Book', 'Book', 'Book', 'Book',
        'Movie', 'Movie', 'Movie', 'Movie',
        'Product', 'Product', 'Product', 'Product'
    ],
    'genre': [
        'Poetry', 'Novel', 'Travel', 'Adventure',
        'Thriller', 'Thriller', 'Crime', 'Action',
        'Smartphone', 'Smartphone', 'Smartphone', 'Smartphone'
    ]
}
df = pd.DataFrame(data)
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df['genre'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(df.index, index=df['title'])
def recommend_item(title, category, num_recommendations=3):
    if title not in indices or df.loc[indices[title], 'category'] != category:
        return [f"No item found for '{title}' in category '{category}'."]
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx and df.loc[s[0], 'category'] == category]
    top_indices = [i[0] for i in sim_scores[:num_recommendations]]
    return df['title'].iloc[top_indices].tolist()
def update_titles(event=None):
    selected_category = category_var.get()
    titles = df[df['category'] == selected_category]['title'].tolist()
    title_menu['values'] = titles
    if titles:
        title_var.set(titles[0])
def get_recommendations():
    selected_title = title_var.get()
    selected_category = category_var.get()
    recommendations = recommend_item(selected_title, selected_category)
    output_box.delete('1.0', tk.END)
    for item in recommendations:
        output_box.insert(tk.END, f"{item}\n")
root = tk.Tk()
root.title("Smart Recommendation System")
tk.Label(root, text="Select Category:").grid(row=0, column=0, padx=10, pady=10)
category_var = tk.StringVar()
category_menu = ttk.Combobox(root, textvariable=category_var, state="readonly")
category_menu['values'] = sorted(df['category'].unique())
category_menu.grid(row=0, column=1)
category_menu.bind('<<ComboboxSelected>>', update_titles)
tk.Label(root, text="Select Title:").grid(row=1, column=0, padx=10, pady=10)
title_var = tk.StringVar()
title_menu = ttk.Combobox(root, textvariable=title_var, state="readonly")
title_menu.grid(row=1, column=1)
recommend_button = tk.Button(root, text="Get Recommendations", command=get_recommendations)
recommend_button.grid(row=2, column=0, columnspan=2, pady=10)
output_box = tk.Text(root, height=6, width=40)
output_box.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
category_var.set(sorted(df['category'].unique())[0])
update_titles()

root.mainloop()
