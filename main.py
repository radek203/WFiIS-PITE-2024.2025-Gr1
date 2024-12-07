import streamlit as st

from backend.models import ImageModel
from backend.scikit_impl import ScikitImpl
from backend.stablediffusion import StableDiffusion
from config import config
from frontend.app_layout import App
from appmain import appmain

def main():
    st.session_state['categories_selected'] = False
    appmain()
    scikit = ScikitImpl(config['debug'])
    scikit.train()
    ids, ratings = scikit.get_top_n_recommendations(config['user_id'], 3)
    print(f"IDs: {ids}", f"Ratings: {ratings}")
    print("Config:", config)

    if 'image_generator' not in st.session_state:
        st.session_state['image_generator'] = StableDiffusion(ImageModel.get_model(config['model_id']), config['debug'])
        st.rerun()


if __name__ == '__main__':
    main()
