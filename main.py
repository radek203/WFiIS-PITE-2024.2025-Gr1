from config import config
from frontend.app_layout import App
import streamlit as st


def main():
    print("Welcome to the program!")
    print("Config:", config)
    app = App()
    app.create_layout()
    

if __name__ == '__main__':
    main()
