import streamlit as st
from backend.scikit_impl import ScikitImpl
from backend.stablediffusion import StableDiffusion, ImageModel
from frontend.app_layout import App


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
        st.session_state['image_generator'] = StableDiffusion(ImageModel.SD35LT, True)

    i = 0 # We need to load here last image id, and only after generating images show them to user
    for prompt in st.session_state['image_generator'].generate_random_prompt(3):
        st.session_state['image_generator'].generate_image(prompt, i)
        i += 1

if __name__ == '__main__':
    main()
