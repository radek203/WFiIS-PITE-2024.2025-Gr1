import os

import streamlit as st

import backend.callbacks as mbc


def display_components(rows, method):
    place_id = 0
    for col in rows:
        method(col, place_id)
        place_id += 1


class App:
    st.session_state['is_image_generate'] = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}
    st.session_state['is_image_rated'] = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}
    st.session_state['image_data'] = {0: [None, 0, 0, ''], 1: [None, 0, 0, ''], 2: [None, 0, 0, '']}
    st.session_state['last_id'] = 0
    st.session_state['category_id'] = 1
    st.session_state['current_user'] = 0
    st.session_state['steps'] = 0
    st.session_state['model'] = None
    st.session_state['decision_buttons'] = False
    st.session_state['tags_rating'] = False
    st.session_state['show_all'] = False

    def __init__(self):
        self.KEY_ID = 0
        st.session_state['last_id'] = mbc.get_number_of_rows()

    def create_image_categories_container(self, parent, place_id):
        tile = parent.container()
        i = st.session_state['last_id'] + 1
        if not st.session_state['is_image_generate'][place_id]:
            tile.write("Generate image")
            prompt, tags = st.session_state['image_generator'].generate_random_prompt(st.session_state['category_id'])
            print(prompt, tags)
            st.session_state['image_generator'].generate_image(prompt, i, st.session_state['steps'])
            st.session_state['is_image_generate'][place_id] = True
            st.session_state['image_data'][place_id] = [f"images/image{i}.png", st.session_state['current_user'], st.session_state['category_id'], "|".join(tags)]
            st.session_state['last_id'] = i
            st.session_state['category_id'] += 1
        img_data = st.session_state['image_data'][place_id]
        tile.image(img_data[0])

    def create_image_tags_container(self, parent, place_id, prompt, tags):
        tile = parent.container()
        i = st.session_state['last_id'] + 1
        if not st.session_state['is_image_generate'][place_id]:
            tile.write("Generate image")
            print(prompt, tags)
            st.session_state['image_generator'].generate_image(prompt, i, st.session_state['steps'])
            st.session_state['is_image_generate'][place_id] = True
            st.session_state['image_data'][place_id] = [f"images/image{i}.png", st.session_state['current_user'], 0, "|".join(tags)]
            st.session_state['last_id'] = i
        img_data = st.session_state['image_data'][place_id]
        tile.image(img_data[0])

    def create_rating_component(self, tile, place_id):
        if not st.session_state['is_image_rated'][place_id]:
            img_data = st.session_state['image_data'][place_id]
            rating = tile.slider("Rating", 1, 10, key=self.KEY_ID)
            self.KEY_ID += 1
            tile.button("Rate", key=self.KEY_ID, use_container_width=True, on_click=mbc.rate_callback, args=(img_data[1], rating, img_data[2], img_data[3], place_id))
            self.KEY_ID += 1

    def create_layout(self):
        container = st.container(border=True)
        container.write("Welcome! Please rate all the images below. Based on your opinion app will generate images for you!")
        box = st.empty()
        if st.session_state['current_user'] == 0:
            users = [str(user) for user in mbc.get_existing_users()]
            box.selectbox("Select user", [""] + users + ["Create New User (Last Id + 1)"], key="user_selection", on_change=mbc.change_user_callback)
        elif 'image_generator' not in st.session_state:
            box.selectbox("Select model", ["", "SD35L", "SD35LT", "SD3MD", "SDXL1"], key="model_selection", on_change=mbc.change_model_callback, args=(box,))
        elif st.session_state['steps'] == 0:
            box.number_input("Number of steps", key="steps_input", min_value=0, step=1, on_change=mbc.change_steps_callback)
        elif st.session_state['decision_buttons']:
            box.selectbox("Select next step", ["", "Generate more images to rate categories", "Go to generating images based on tags from best rated categories only", "Show all generated images"], key="next_step_selection", on_change=mbc.next_step_selection)
        elif st.session_state['show_all']:
            png_files = [file for file in os.listdir("images") if file.endswith('.png')]
            images_box = box.container(border=True)
            row = images_box.columns(3)
            i = 0
            for file in png_files:
                if i % 3 == 0:
                    row = images_box.columns(3)
                row[i % 3].container().image(f"images/{file}")
                i += 1
        else:
            images_box = box.container(border=True)
            row1 = images_box.columns(3)
            row2 = images_box.columns(3)
            row3 = images_box.columns(3)
            if st.session_state['tags_rating']:
                prompts, tags = st.session_state['image_generator'].generate_prompt_from_best_tags(st.session_state['current_user'])
                place_id = 0
                for col in row1 + row2 + row3:
                    self.create_image_tags_container(col, place_id, prompts[place_id], tags[place_id])
                    place_id += 1
            else:
                display_components(row1 + row2 + row3, self.create_image_categories_container)
            display_components(row1 + row2 + row3, self.create_rating_component)
