import streamlit as st

import backend.callbacks as mbc
from config import config


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

    def __init__(self):
        self.KEY_ID = 0
        st.session_state['last_id'] = mbc.get_number_of_rows()

    def create_image_container(self, parent, place_id):
        tile = parent.container()
        i = st.session_state['last_id'] + 1
        if not st.session_state['is_image_generate'][place_id]:
            tile.write("Generate image")
            prompt, tags = st.session_state['image_generator'].generate_random_prompt(1, st.session_state['category_id'])
            prompt = prompt[0]
            tags = tags[0]
            print(prompt, tags)
            st.session_state['image_generator'].generate_image(prompt, i)
            st.session_state['is_image_generate'][place_id] = True
            st.session_state['image_data'][place_id] = [f"images/image{i}.png", config['user_id'], st.session_state['category_id'], "|".join(tags)]
            st.session_state['last_id'] = i
            st.session_state['category_id'] += 1
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
        container.write("Welcome! Please click 👍 if you like the image and if it is not what you are looking for click 👎. Remember there are two tabs to choose from. Based on your opinion app will generate image for you!")
        layout = st.container(border=True)
        if 'image_generator' not in st.session_state:
            layout.write("Loading Image Generator...")
        else:
            row1 = layout.columns(3)
            row2 = layout.columns(3)
            row3 = layout.columns(3)
            display_components(row1 + row2 + row3, self.create_image_container)
            display_components(row1 + row2 + row3, self.create_rating_component)
