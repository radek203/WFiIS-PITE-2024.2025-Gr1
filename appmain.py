from frontend.app_layout import App
import streamlit as st

def appmain():
    print("Welcome to the program!")
    app = App()
    app.create_layout()

if __name__ == "__main__":
    appmain()