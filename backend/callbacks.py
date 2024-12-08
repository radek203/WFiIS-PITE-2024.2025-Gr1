import pandas as pd
import streamlit as st

def rate_callback(user_id, ratings, category_id, tags, place_id):
    new_row = {
        "userId": user_id,
        "categoryId": category_id,
        "rating": ratings,
        "tags": tags
    }
    st.session_state['is_image_rated'][place_id] = True
    save_row_to_file(new_row)
    regenerate_images()

def regenerate_images():
    if False not in st.session_state['is_image_rated'].values():
        for i in range(9):
            st.session_state['is_image_rated'][i] = False
            st.session_state['is_image_generate'][i] = False
        st.session_state['category_id'] = 1
        st.session_state['last_id'] =+ 1
        print(st.session_state['is_image_rated'], st.session_state['is_image_generate'])

def save_row_to_file(new_row):
    data = pd.read_csv("data/ratings.csv")
    new_row_df = pd.DataFrame([new_row], columns=data.columns)
    updated_data = pd.concat([data, new_row_df], ignore_index=True)
    updated_data.to_csv("data/ratings.csv", index=False)


def get_number_of_rows():
    data = pd.read_csv("data/ratings.csv")
    return data.shape[0]
