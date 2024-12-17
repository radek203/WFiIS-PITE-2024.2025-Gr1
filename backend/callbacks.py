import pandas as pd
import streamlit as st

from backend.utils import get_top_n_categories
from backend.models import ImageModel
from backend.stablediffusion import StableDiffusion
from config import config


def find_tag_category_id(tag):
    for i in range(1, 10):
        filename = f"data/cat{i}.csv"
        with open(filename, "r") as file:
            file_content = file.read()
            if tag in file_content:
                return i


def rate_callback(user_id, ratings, category_id, tags, place_id):
    categories = []
    for tag in tags.split('|'):
        category_id = find_tag_category_id(tag)
        if category_id is not None:
            categories.append(category_id)
    if all(cat == categories[0] for cat in categories):
        final = str(categories[0])
    else:
        final = "|".join(map(str,categories))
    new_row = {
        "userId": user_id,
        "categoryId": final,
        "rating": ratings,
        "tags": tags
    }
    st.session_state['is_image_rated'][place_id] = True
    save_row_to_file(new_row)
    regenerate_images()


def regenerate_images():
    if False not in st.session_state['is_image_rated'].values():
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
    if selected_user == "Create New User":
        existing_users = get_existing_users()
        selected_user = 1 if len(existing_users) == 0 else (int(existing_users[-1]) + 1)
    st.session_state['current_user'] = int(selected_user)
    print("Selected user:", selected_user)


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



