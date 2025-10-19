import streamlit as st

# 设置页面配置
st.set_page_config(
    page_title="智能农业助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏Streamlit默认样式
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

# 只显示聊天机器人插件
st.markdown("""
<div style="width: 100%; height: 100vh;">
    <iframe
        src="http://www.baidu.com"
        style="width: 100%; height: 100vh;"
        frameborder="0"
        allow="microphone">
    </iframe>
</div>
""", unsafe_allow_html=True)