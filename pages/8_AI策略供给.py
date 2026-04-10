import streamlit as st

st.set_page_config(
    page_title="智能农业助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏Streamlit默认元素
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {
        padding: 0;
        margin: 0;
    }
    .block-container {
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 0;
        padding-right: 0;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 嵌入您的聊天机器人
st.markdown("""
<div style="width: 100%; height: 100vh;">
    <iframe
         src="https://udify.app/chat/Ni87WoW126qxVLnf"
         style="width: 100%; height: 100%; min-height: 700px"
         frameborder="0"
         allow="microphone">
    </iframe>
</div>
""", unsafe_allow_html=True)
