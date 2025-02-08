import streamlit as st
import pickle
import numpy as np
import pandas as pd 

st.set_page_config(layout="wide")
st.header("Book Recommender System")
st.markdown('''
#### The site using collaborative filtering suggests books from our catalog.
#### We recommend the top 50 books for everyone as well.
''')

# Load models
popular = pickle.load(open('popular.pkl', 'rb'))
book = pickle.load(open('books.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))  # Fixed variable name

# Sidebar for top 50 books
st.sidebar.title("Top 50 Books")
if st.sidebar.button("Show"):
    cols_per_row = 5
    num_rows = min(10, len(popular) // cols_per_row)  # Avoid out-of-range errors

    for row in range(num_rows):
        cols = st.columns(cols_per_row)
        for col in range(cols_per_row):
            book_idx = row * cols_per_row + col
            if book_idx < len(popular):
                with cols[col]:
                    st.image(popular.iloc[book_idx]['Image-URL-M'])
                    st.text(popular.iloc[book_idx]['Book-Title'])
                    st.text(popular.iloc[book_idx]['Book-Author'])

# Function to recommend books
def recommend(book_name):
    indices = np.where(pt.index == book_name)[0]
    if len(indices) == 0:
        st.error("Book not found in dataset!")
        return []
    
    index = indices[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    data = []
    for i in similar_items:
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]

        item = [
            temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
            temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
            temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
        ]
        data.append(item)

    return data

# Dropdown for book selection
book_list = pt.index.values
st.sidebar.title("Similar Book Suggestions")
select_book = st.sidebar.selectbox("Select a Book From The Dropdown", book_list)

if st.sidebar.button("Recommend Me"):
    book_recommend = recommend(select_book)
    cols = st.columns(len(book_recommend))  # Dynamic column count

    for col_idx, book in enumerate(book_recommend):
        with cols[col_idx]:
            st.image(book[2])
            st.text(book[0])
            st.text(book[1])



