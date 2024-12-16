import pandas as pd
import streamlit as st

from backend.models import ImageModel
from backend.scikit_impl import ScikitImpl
from backend.stablediffusion import StableDiffusion
from config import config


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
        calculate_ratings(st.session_state['current_user'])
        print(get_top_n_categories(3, st.session_state['current_user']))
        for i in range(9):
            st.session_state['is_image_rated'][i] = False
            st.session_state['is_image_generate'][i] = False
        st.session_state['category_id'] = 1
        st.session_state['decision_buttons'] = True


def save_row_to_file(new_row):
    data = pd.read_csv("data/ratings.csv")
    new_row_df = pd.DataFrame([new_row], columns=data.columns)
    updated_data = pd.concat([data, new_row_df], ignore_index=True)
    updated_data.to_csv("data/ratings.csv", index=False)


def get_number_of_rows():
    data = pd.read_csv("data/ratings.csv")
    return data.shape[0]


def get_existing_users():
    data = pd.read_csv("data/ratings.csv")
    return data.userId.unique()


def change_user_callback():
    selected_user = st.session_state["user_selection"]
    if selected_user == "Create New User (Last Id + 1)":
        selected_user = int(get_existing_users()[-1]) + 1
    st.session_state['current_user'] = int(selected_user)
    print("Selected user:", selected_user)


def calculate_ratings(user_id):
    scikit = ScikitImpl(config['debug'])
    scikit.train()
    ids, ratings = scikit.get_top_n_ratings(user_id, 3)
    print(f"IDs: {ids}", f"Ratings: {ratings}")


def change_model_callback(layout):
    layout.write("Loading Image Generation Model...")
    selected_model = st.session_state["model_selection"]
    st.session_state['model'] = selected_model
    st.session_state['image_generator'] = StableDiffusion(ImageModel.get_model(selected_model), config['debug'])
    print("Selected model:", selected_model)


def change_steps_callback():
    steps = st.session_state['steps_input']
    st.session_state['steps'] = int(steps)
    print("Steps:", steps)


def next_step_selection():
    next_step = st.session_state['next_step_selection']
    st.session_state['decision_buttons'] = False
    st.session_state['tags_rating'] = False
    st.session_state['show_all'] = False
    if next_step.startswith("Show"):
        st.session_state['show_all'] = True
    else:
        st.session_state['tags_rating'] = True


def get_top_n_categories(n, user_id):
    data = pd.read_csv("data/ratings.csv")
    specific_user_data = data[data["userId"] == user_id]
    category_sum = specific_user_data.groupby("categoryId")["rating"].sum().reset_index()
    top_category = category_sum.sort_values(by = "rating", ascending = False).head(n)
    return top_category

def get_top_n_recommendations(n, user_id):
    sc = ScikitImpl(True)
    sc.train()
    return sc.get_top_n_ratings(user_id, n)