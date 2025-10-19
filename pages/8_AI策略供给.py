import streamlit as st

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

# 使用meta标签和更宽松的sandbox策略
st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Security-Policy" content="default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;">
    <meta http-equiv="X-Frame-Options" content="ALLOW-FROM http://119.45.173.154">
    <style>
        body, html {
            margin: 0;
            padding: 0;
            height: 100%;
            overflow: hidden;
            background: white;
        }
    </style>
</head>
<body>
    <!-- 方法1：使用embed标签 -->
    <embed src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" 
           style="width:100%; height:100vh; border:none;">
    
    <!-- 方法2：备用iframe -->
    <iframe src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" 
            style="width:100%; height:100vh; border:none; display:none;"
            id="backupFrame"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals allow-orientation-lock allow-pointer-lock allow-presentation allow-top-navigation">
    </iframe>
    
    <script>
        // 检查embed是否工作
        setTimeout(function() {
            const embed = document.querySelector('embed');
            const iframe = document.getElementById('backupFrame');
            
            if (!embed || embed.style.visibility === 'hidden') {
                iframe.style.display = 'block';
            }
            
            // 最终备用方案：显示链接
            setTimeout(function() {
                if (!document.querySelector('iframe') && !document.querySelector('embed')) {
                    document.body.innerHTML = '<div style="padding:20px;text-align:center;"><h3>无法嵌入内容</h3><p><a href="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" target="_blank">点击这里直接访问聊天机器人</a></p></div>';
                }
            }, 5000);
        }, 3000);
    </script>
</body>
</html>
""", height=800)