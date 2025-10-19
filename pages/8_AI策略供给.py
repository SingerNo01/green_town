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

# 检查目标URL是否可访问
try:
    response = requests.get("http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV", timeout=5)
    if response.status_code == 200:
        st.success("目标URL可访问，正在加载...")
    else:
        st.error(f"目标URL返回状态码: {response.status_code}")
except Exception as e:
    st.error(f"无法访问目标URL: {e}")

# 嵌入iframe
st.markdown("""
<div style="width: 100%; height: 100vh;">
    <iframe
        src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV"
        style="width: 100%; height: 100vh; border: none;"
        frameborder="0"
        allow="microphone"
        onload="console.log('iframe加载完成')"
        onerror="console.log('iframe加载失败')">
    </iframe>
</div>

<script>
    // 在浏览器控制台输出调试信息
    console.log('开始加载iframe...');
    console.log('目标URL:', 'http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV');
</script>
""", unsafe_allow_html=True)