import os

import streamlit as st

import backend.callbacks as cb
from backend.utils import get_number_of_rows, get_user_images


def display_components(rows, method, prompts, tags, categories):
    place_id = 0
    for col in rows:
        if place_id < len(prompts):
            method(col, place_id, prompts[place_id], tags[place_id], categories[place_id])
        else:
            method(col, place_id, "", "", "")
        place_id += 1


class App:
    st.session_state['is_image_generate'] = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}
    st.session_state['is_image_rated'] = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}
    st.session_state['image_data'] = {}
    st.session_state['last_id'] = 0
    st.session_state['current_user'] = 0
    st.session_state['steps'] = 0
    st.session_state['model'] = None
    st.session_state['decision_buttons'] = False
    st.session_state['tags_rating'] = False
    st.session_state['show_all'] = False

    def __init__(self):
        self.KEY_ID = 0
        st.session_state['last_id'] = get_number_of_rows()

    def create_image_container(self, parent, place_id, prompt, tags, categories):
        tile = parent.empty()
        i = st.session_state['last_id'] + 1
        if not st.session_state['is_image_generate'][place_id]:
            tile.write("Generating image...")
            print(prompt, tags)
            st.session_state['image_generator'].generate_image(prompt, i, st.session_state['steps'])
            st.session_state['is_image_generate'][place_id] = True
            st.session_state['image_data'][place_id] = [i, '|'.join(map(str, categories)), "|".join(tags)]
            st.session_state['last_id'] = i
        img_data = st.session_state['image_data'][place_id]
        tile.image(f"images/image{img_data[0]}.png")

    def create_rating_component(self, tile, place_id, prompt, tags, categories):
        if not st.session_state['is_image_rated'][place_id]:
            rating = tile.slider("Rating", 1, 10, key=self.KEY_ID)
            self.KEY_ID += 1
            tile.button("Rate", key=self.KEY_ID, use_container_width=True, on_click=cb.rate_callback, args=(rating, st.session_state['image_data'][place_id], place_id))
            self.KEY_ID += 1

    def create_layout(self):
        container = st.container(border=True)
        container.write("Welcome! Please rate all the images below. Based on your opinion app will generate images for you!")
        box = st.empty()
        if st.session_state['current_user'] == 0:
            users = [str(user) for user in cb.get_existing_users()]
            box.selectbox("Select user", [""] + users + ["Create New User"], key="user_selection", on_change=cb.change_user_callback)
        elif 'image_generator' not in st.session_state:
            box.selectbox("Select model", ["", "SD35L", "SD35LT", "SD3MD", "SDXL1"], key="model_selection", on_change=cb.change_model_callback, args=(box,))
        elif st.session_state['steps'] == 0:
            box.number_input("Number of steps", key="steps_input", min_value=0, step=1, on_change=cb.change_steps_callback)
        elif st.session_state['decision_buttons']:
            box.selectbox("Select next step", ["", "Generate more images to rate categories", "Go to generating images based on tags from best rated categories only", "Show all generated images"], key="next_step_selection", on_change=cb.next_step_selection_callback)
        elif st.session_state['show_all']:
            images_box = box.container(border=True)
            row = images_box.columns(3)
            i = 0
            for img_id in get_user_images(st.session_state['current_user']):
                if os.path.isfile(f"images/image{img_id}.png"):
                    if i % 3 == 0:
                        row = images_box.columns(3)
                    row[i % 3].container().image(f"images/image{img_id}.png")
                    i += 1
        else:
            images_box = box.container(border=True)
            row1 = images_box.columns(3)
            row2 = images_box.columns(3)
            row3 = images_box.columns(3)
            if st.session_state['tags_rating']:
                prompts, tags, categories = st.session_state['image_generator'].generate_prompt_from_best_tags(st.session_state['current_user'])
            else:
                prompts, tags, categories = st.session_state['image_generator'].generate_random_prompts()
            display_components(row1 + row2 + row3, self.create_image_container, prompts, tags, categories)
            display_components(row1 + row2 + row3, self.create_rating_component, [], [], [])
