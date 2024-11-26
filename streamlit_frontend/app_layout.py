import streamlit as st


class App:

    def __init__(self):
        self.KEY_ID = 0


    def create_image_container(self, parent):
        tile = parent.container()
        tile.image("placeholder.png")
        yes, no = tile.columns(2)
        yes.button("Like", key = self.KEY_ID)
        self.KEY_ID += 1
        no.button("Dislike", key = self.KEY_ID)
        self.KEY_ID += 1


    def create_layout(self):
        container = st.container(border=True)
        container.write("Welcome!")
        layout = st.container(border = True)
        row1 = layout.columns(3)
        row2 = layout.columns(3)
        row3 = layout.columns(3)
        for col in row1 + row2 + row3:
            self.create_image_container(col)
