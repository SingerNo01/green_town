import streamlit as st

st.set_page_config(
    page_title="智能农业助手",
    layout="centered"
)

# 如果iframe无法加载，提供直接访问按钮
st.title("🤖 智能农业助手")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div style="width: 100%; height: 600px; border: 1px solid #ddd; border-radius: 10px; overflow: hidden;">
        <iframe
            src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV"
            style="width: 100%; height: 100%;"
            frameborder="0"
            allow="microphone">
        </iframe>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.info("""
    **如果无法显示聊天窗口：**
    
    请点击下方按钮直接访问
    """)
    
    if st.button("🚀 直接访问聊天机器人", use_container_width=True):
        st.markdown('[点击打开](http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV)')
    
    st.warning("""
    **可能的原因：**
    - 网站安全策略限制
    - 网络连接问题
    - 浏览器安全设置
    """)