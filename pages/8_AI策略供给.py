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
    .redirect-button {
        padding: 20px;
        text-align: center;
        background: #f0f2f6;
        border-radius: 10px;
        margin: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 直接显示重定向界面
st.markdown("""
<div style="text-align: center; padding: 50px;">
    <h2>智能农业助手</h2>
    <p>正在为您加载聊天机器人...</p>
    <p>如果页面没有自动跳转，请点击下方按钮</p>
</div>
""", unsafe_allow_html=True)

# 自动重定向
st.components.v1.html("""
<script>
    // 尝试在新标签页打开
    window.open("http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV", "_blank");
    
    // 显示提示信息
    setTimeout(function() {
        document.body.innerHTML = '<div style="padding:50px;text-align:center;"><h3>聊天机器人已在新标签页打开</h3><p>如果浏览器阻止了弹出窗口，请允许该网站的弹出窗口或点击下方按钮</p><button onclick="window.open(\'http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV\', \'_blank\')" style="padding:10px 20px;background:#ff4b4b;color:white;border:none;border-radius:5px;cursor:pointer;">打开聊天机器人</button></div>';
    }, 1000);
</script>
""", height=400)

# 添加手动重定向按钮
if st.button("手动打开聊天机器人"):
    st.components.v1.html("""
    <script>
        window.open("http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV", "_blank");
    </script>
    """)