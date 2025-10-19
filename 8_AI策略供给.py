import streamlit as st

st.set_page_config(
    page_title="智能农业助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 0;
        padding-right: 0;
        max-width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 尝试直接访问链接
st.markdown("""
<div style="width: 100%; height: 100vh;">
    <iframe
        src="https://udify.app/chatbot/6MCrcJyUrhQwiY5P"
        style="width: 100%; height: 100vh;"
        frameborder="0"
        allow="microphone">
    </iframe>
</div>
""", unsafe_allow_html=True)

# 添加备用访问方式
st.markdown("""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <a href="https://udify.app/chatbot/6MCrcJyUrhQwiY5P" target="_blank" 
       style="background-color: #4CAF50; color: white; padding: 10px 15px; 
              text-decoration: none; border-radius: 5px; font-size: 14px;">
        🔗 如果无法显示，点击这里直接访问
    </a>
</div>
""", unsafe_allow_html=True)