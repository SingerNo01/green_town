import streamlit as st
import os

# 禁用安全限制以允许 HTTP 内容
os.environ['STREAMLIT_SERVER_ENABLE_XSRF'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'

st.set_page_config(
    page_title="智能农业助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏Streamlit默认元素并添加允许 HTTP 的样式
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
    /* 允许混合内容 */
    iframe {
        -webkit-security-policy: mixed-content;
    }
</style>
""", unsafe_allow_html=True)

# 嵌入您的聊天机器人
st.markdown("""
<div style="width: 100%; height: 100vh;">
    <iframe
        src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV"
        style="width: 100%; height: 100vh; border: none;"
        frameborder="0"
        allow="microphone *"
        allowfullscreen>
    </iframe>
</div>
""", unsafe_allow_html=True)