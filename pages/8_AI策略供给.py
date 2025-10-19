import streamlit as st
import requests

st.set_page_config(
    page_title="智能农业助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 隐藏默认元素
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

# 尝试获取页面内容并直接显示
try:
    response = requests.get("http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV", timeout=10)
    if response.status_code == 200:
        # 直接显示HTML内容
        st.components.v1.html(response.text, height=800, scrolling=True)
    else:
        st.error("无法获取页面内容")
except Exception as e:
    st.error(f"获取页面内容失败: {e}")
    
    # 备用：显示重定向按钮
    st.warning("点击下方按钮直接访问聊天机器人")
    if st.button("打开聊天机器人"):
        st.components.v1.html("""
        <script>
            window.open("http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV", "_blank");
        </script>
        """)