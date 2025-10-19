import streamlit as st
import requests

st.set_page_config(
    page_title="智能农业助手",
    layout="wide"
)

def check_website_accessible():
    """检查网站是否可访问"""
    try:
        response = requests.get("http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV", timeout=5)
        return response.status_code == 200
    except:
        return False

# 检查网站可访问性
if check_website_accessible():
    st.markdown("""
    <style>
    .iframe-container {
        width: 100%;
        height: 100vh;
    }
    </style>
    <div class="iframe-container">
        <iframe
            src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV"
            style="width: 100%; height: 100vh; border: none;"
            frameborder="0"
            allow="microphone">
        </iframe>
    </div>
    """, unsafe_allow_html=True)
else:
    st.error("无法连接到聊天机器人服务器")
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h3>备用访问方式</h3>
        <a href="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" target="_blank">
            <button style="padding: 10px 20px; font-size: 16px;">
                🚀 直接访问聊天机器人
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)