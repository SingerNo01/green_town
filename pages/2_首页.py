# pages/首页.py
import streamlit as st

st.set_page_config(
    page_title="首页 - 生态增值，农策共荣",
    layout="wide"
)

## 主标题
st.title("生态增值，农策共荣")
st.subheader("农业生态产品价值实现综合效益评估与策略供给模型")

## 导航说明
st.divider()
st.write("请单击左侧边栏导航到不同功能页面：")
st.markdown("""
    - **首页** - 系统概览和导航
    - **层次分析法计算主观权重** - 使用AHP方法计算主观权重
    - **熵权法计算客观权重** - 基于数据熵值计算客观权重  
    - **组合权重计算** - 结合主客观权重得出组合权重
    - **综合得分评估** - 基于权重计算综合得分
    - **策略建议生成** - AI智能生成策略建议
""")
st.divider()

## 页脚
st.divider()
st.caption("© 2025 生态增值，农策共荣 - 所有权利保留")