import streamlit as st

st.set_page_config(layout="wide")

st.components.v1.html("""
<div style="width: 100%; height: 100vh;">
    <iframe 
        src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV"
        style="width: 100%; height: 100vh; border: none;"
        frameborder="0"
        allow="microphone">
    </iframe>
</div>
""", height=700)