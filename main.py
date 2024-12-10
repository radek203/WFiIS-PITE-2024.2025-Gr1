from config import config
from frontend.app_layout import App
import streamlit as st


def main():
    print("Welcome to the program!")
    print("Config:", config)
    app = App()
    st.session_state['amout_of_rated_categories'] = 0
    app.create_layout()
    

if __name__ == '__main__':
    main()
