import streamlit as st
import backend.callbacks as mbc


class App:
    st.session_state['is_image_generate'] = {0: False, 1: False, 2: False}
    st.session_state['image_path'] = {0: None, 1: None, 2: None}
    def __init__(self):
        self.KEY_ID = 0
        # We need to link this with generating images to get generated images data - id, user_id, category_id, tags
        # self.images = mbc.get_image_data([0,1,2])



    def create_tabs(self):
        tab1, tab2 = st.tabs(["Tab 1", "Tab 2"])
        with tab1:
            st.header("Tab 1")
        with tab2:
            st.header("Tab 2")

    def create_image_container(self, parent,place_id):
        tile = parent.container()
        i = mbc.get_number_of_rows() + 1
        if(st.session_state['is_image_generate'][place_id]==False):
            tile.write("Generate image")
            prompt = st.session_state['image_generator'].generate_random_prompt(1)
            st.session_state['image_generator'].generate_image(prompt, i)
            st.session_state['is_image_generate'][place_id] = True
            cur_filename, user_id, category_id, tags = mbc.get_image_data(i)
            st.session_state['image_path'][place_id] = cur_filename
        tile.image(st.session_state['image_path'][place_id])
        yes, no = tile.columns(2)
        yes.button("", key=self.KEY_ID, icon="👍", use_container_width=True, on_click=mbc.like_callback, args=(st.session_state['image_path'][place_id], 1, 1, 1))
        self.KEY_ID += 1
        no.button("", key=self.KEY_ID, icon="👎", use_container_width=True, on_click=mbc.dislike_callback, args=(st.session_state['image_path'][place_id], 1, 1, 1))
        self.KEY_ID += 1

    def create_layout(self):
        container = st.container(border=True)
        container.write("Welcome! Please click 👍 if you like the image and if it is not what you are looking for click 👎. Remember there are two tabs to choose from. Based on your opinion app will generate image for you!")
        layout = st.container(border=True)
        if 'image_generator' not in st.session_state:
            layout.write("Loading Image Generator...")
        else:
            row1 = layout.columns(3)
            #row2 = layout.columns(3)
            #row3 = layout.columns(3)
            #for col in row1 + row2 + row3:
            place_id = 0
            for col in row1:
                self.create_image_container(col,place_id)
                place_id += 1
