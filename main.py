import streamlit as st
from scikit_impl import ScikitImpl
from stablediffusion import StableDiffusion
from streamlit_frontend.app_layout import App


def main():
    print("Welcome to the program!")
    app = App()
    app.create_tabs()
    app.create_layout()
    scikit = ScikitImpl(True)
    scikit.train()
    ids, ratings = scikit.get_top_n_recommendations(1, 3)
    print(f"IDs: {ids}", f"Ratings: {ratings}")

    if 'image_generator' not in st.session_state:
        st.session_state['image_generator'] = StableDiffusion()

    st.session_state['image_generator'].generate_image("dachshund in the santa claus hat writing a python code on the computer", "dachshund")
    st.session_state['image_generator'].generate_image("Big white cat in santa clauss hat", "cat")


if __name__ == '__main__':
    main()
