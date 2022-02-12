import streamlit as st

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self): 
        page = st.sidebar.selectbox(
            'App Navigation', 
            self.apps, 
            format_func=lambda page: page['title']
        )

        page['function']()