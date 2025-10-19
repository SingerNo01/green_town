import streamlit as st
import os

# 彻底禁用安全限制
os.environ['STREAMLIT_SERVER_ENABLE_XSRF'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'

st.set_page_config(
    page_title="智能农业助手",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 更彻底的样式和安全性覆盖
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
    /* 禁用安全策略 */
    iframe {
        security: allow-same-origin allow-scripts allow-forms allow-popups;
    }
</style>

<script>
    // 强制允许混合内容
    document.addEventListener('DOMContentLoaded', function() {
        const iframe = document.querySelector('iframe');
        if (iframe) {
            iframe.setAttribute('security', 'allow-same-origin allow-scripts');
        }
    });
</script>
""", unsafe_allow_html=True)

# 使用 JavaScript 动态创建 iframe 作为备选方案
st.components.v1.html("""
<div style="width: 100%; height: 100vh;">
    <iframe
        src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV"
        style="width: 100%; height: 100vh; border: none;"
        frameborder="0"
        allow="microphone *"
        allowfullscreen
        sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals">
    </iframe>
</div>
""", height=800)

# 备用嵌入方法
st.markdown("""
<div style="width: 100%; height: 100vh;">
    <object 
        data="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" 
        style="width: 100%; height: 100vh; border: none;">
        <embed 
            src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" 
            style="width: 100%; height: 100vh;">
    </object>
</div>
""", unsafe_allow_html=True)