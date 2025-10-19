import streamlit as st

st.set_page_config(layout="wide")

st.title("测试页面")

# 方法1：直接iframe
st.markdown("### 方法1：直接iframe")
st.components.v1.iframe(
    "http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV",
    height=600,
    scrolling=True
)

# 方法2：HTML方式
st.markdown("### 方法2：HTML方式")
st.markdown("""
<div style="border: 2px solid red; height: 600px;">
    <iframe src="http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV" 
            style="width:100%; height:100%; border:none;"></iframe>
</div>
""", unsafe_allow_html=True)

# 方法3：直接链接
st.markdown("### 方法3：直接访问")
st.markdown('[点击这里直接访问聊天机器人](http://119.45.173.154/chatbot/Rr8QS2s9GIvD9ndV)')