import streamlit as st

st.set_page_config(
    page_title="智能农业助手",
    layout="centered"
)

# 创建自动重定向页面
st.markdown("""
<div style="text-align: center; padding: 50px;">
    <h1>🤖 智能农业助手</h1>
    <p>正在跳转到聊天机器人...</p>
    <div style="margin: 30px 0;">
        <a href="https://udify.app/chatbot/6MCrcJyUrhQwiY5P" 
           style="background-color: #4CAF50; color: white; padding: 15px 30px; 
                  text-decoration: none; border-radius: 5px; font-size: 16px;">
            🚀 点击进入聊天机器人
        </a>
    </div>
    <p style="color: #666; margin-top: 20px;">
        如果页面没有自动跳转，请点击上方按钮
    </p>
</div>

<script>
    // 自动跳转
    setTimeout(function() {
        window.open('https://udify.app/chatbot/6MCrcJyUrhQwiY5P', '_blank');
    }, 2000);
</script>
""", unsafe_allow_html=True)