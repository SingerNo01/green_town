import streamlit as st

st.set_page_config(
    page_title="智能农业助手",
    layout="centered"
)

# 使用JavaScript重定向
st.components.v1.html("""
<script>
    window.open('https://udify.app/chatbot/6MCrcJyUrhQwiY5P', '_blank');
</script>

<div style="text-align: center; padding: 100px;">
    <h2>正在打开智能农业助手...</h2>
    <p>如果浏览器阻止了弹出窗口，请允许该网站的弹出窗口或<a href="https://udify.app/chatbot/6MCrcJyUrhQwiY5P" target="_blank">点击这里手动打开</a></p>
</div>
""", height=400)