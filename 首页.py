# app.py
import streamlit as st
import os
import zipfile
from io import BytesIO

## 设置页面配置
st.set_page_config(
    page_title="生态增值，农策共荣",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

## 主标题
st.title("生态增值，农策共荣")
st.subheader("农业生态产品价值实现综合效益评估与策略供给模型")

## 导航说明
st.divider()
st.write("请单击左侧边栏导航到不同功能页面：")
st.markdown("""
    - 层次分析法计算主观权重
    - 熵权法计算客观权重
    - 组合权重计算
    - 综合得分评估
    - 策略建议生成
""")
st.divider()

## 页脚
st.divider()
st.caption("© 2025 生态增值，农策共荣 - 所有权利保留")