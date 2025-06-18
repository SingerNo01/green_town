import streamlit as st

st.title("DeepSeek Chat Embedded")

# 嵌入 DeepSeek 聊天窗口（如果官方提供）
deepseek_url = "https://chat.deepseek.com/embed"  # 假设 DeepSeek 提供 iframe
st.components.v1.iframe(deepseek_url, width=700, height=500)