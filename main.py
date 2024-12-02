import streamlit as st

from backend.models import ImageModelSD3MD, ImageModelSDXL1, ImageModelSD35LT, ImageModelSD35L
from backend.scikit_impl import ScikitImpl
from backend.stablediffusion import StableDiffusion
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
        st.session_state['image_generator'] = StableDiffusion(ImageModelSD35LT(), True)
        st.rerun()

if __name__ == '__main__':
    main()
