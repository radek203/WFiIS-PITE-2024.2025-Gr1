import streamlit as st

from backend.models import ImageModel
from backend.stablediffusion import StableDiffusion
from backend.utils import save_row_to_file, get_existing_users
from config import config


def rate_callback(ratings, img_data, place_id):
    st.session_state['is_image_rated'][place_id] = True
    save_row_to_file({
        "id": img_data[0],
        "userId": st.session_state['current_user'],
        "categoryId": img_data[1],
        "rating": ratings,
        "tags": img_data[2]
    })
    regenerate_images()


def regenerate_images():
    if False not in st.session_state['is_image_rated'].values():
        for i in range(9):
            st.session_state['is_image_rated'][i] = False
            st.session_state['is_image_generate'][i] = False
        st.session_state['category_id'] = 1
        st.session_state['decision_buttons'] = True


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


def next_step_selection_callback():
    next_step = st.session_state['next_step_selection']
    st.session_state['decision_buttons'] = False
    st.session_state['tags_rating'] = False
    st.session_state['show_all'] = False
    if next_step.startswith("Show"):
        st.session_state['show_all'] = True
    else:
        st.session_state['tags_rating'] = True
