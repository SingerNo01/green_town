import streamlit as st
import requests
import base64

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

# 方法1：使用JavaScript动态创建iframe
st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
        }
        #chatbotContainer {
            width: 100%;
            height: 100vh;
        }
    </style>
</head>
<body>
    <div id="chatbotContainer"></div>
    
    <script>
        // 方法1：使用JavaScript动态创建iframe
        function createIframe() {
            const container = document.getElementById('chatbotContainer');
            const iframe = document.createElement('iframe');
            iframe.src = "http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV";
            iframe.style.width = "100%";
            iframe.style.height = "100vh";
            iframe.style.border = "none";
            iframe.allow = "microphone";
            iframe.referrerPolicy = "no-referrer";
            
            container.appendChild(iframe);
            
            // 添加错误处理
            iframe.onload = function() {
                console.log('Iframe loaded successfully');
            };
            
            iframe.onerror = function() {
                console.log('Iframe failed to load');
                // 备用方案：重定向
                setTimeout(() => {
                    window.location.href = "http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV";
                }, 2000);
            };
        }
        
        // 延迟创建iframe以避免阻塞
        setTimeout(createIframe, 100);
    </script>
</body>
</html>
""", height=800)