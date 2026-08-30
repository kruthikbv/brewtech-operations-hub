import streamlit as st

def initialize():
    for key, value in {'is_authenticated': False, 'access_token': None, 'refresh_token': None, 'current_user': None}.items(): st.session_state.setdefault(key, value)
def login(tokens, user):
    st.session_state.is_authenticated = True; st.session_state.access_token = tokens['access']; st.session_state.refresh_token = tokens.get('refresh'); st.session_state.current_user = user
def logout():
    for key in ('is_authenticated', 'access_token', 'refresh_token', 'current_user'): st.session_state[key] = False if key == 'is_authenticated' else None
