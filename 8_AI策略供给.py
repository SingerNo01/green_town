import streamlit as st
import webbrowser

st.set_page_config(
    page_title="智能农业助手",
    layout="centered"
)

st.title("🤖 智能农业助手")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("聊天机器人")
    st.write("点击下方按钮打开智能农业助手")
    
    if st.button("🎯 打开聊天机器人", use_container_width=True):
        webbrowser.open_new_tab("https://udify.app/chatbot/6MCrcJyUrhQwiY5P")
    
    st.info("""
    **功能特色：**
    - 智能农业咨询
    - 生态产业分析
    - 政策建议
    - 技术指导
    """)

with col2:
    st.subheader("使用说明")
    st.markdown("""
    1. 点击左侧按钮打开聊天机器人
    2. 在新窗口中与AI助手对话
    3. 可同时保留此页面参考
    
    **支持的问题类型：**
    - 农业生产技术
    - 市场分析
    - 政策解读
    - 生态保护
    """)