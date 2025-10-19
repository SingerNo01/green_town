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

## 创建侧边栏导航
with st.sidebar:
    st.title("🌱 导航菜单")
    
    # 导航选项
    selected = st.radio(
        "选择功能页面:",
        ["首页", "层次分析法计算主观权重", "熵权法计算客观权重", "组合权重计算", "综合得分评估", "策略建议生成"],
        index=0
    )
    
    st.divider()
    st.markdown("### 使用说明")
    st.info("请从上方选择需要的功能模块")

## 根据选择显示不同页面
if selected == "首页":
    ## 主标题
    st.title("生态增值，农策共荣")
    st.subheader("农业生态产品价值实现综合效益评估与策略供给模型")

    ## 导航说明
    st.divider()
    st.write("请从左侧边栏选择不同功能页面：")
    st.markdown("""
        - **层次分析法计算主观权重** - 使用AHP方法计算主观权重
        - **熵权法计算客观权重** - 基于数据熵值计算客观权重
        - **组合权重计算** - 结合主客观权重得出组合权重
        - **综合得分评估** - 基于权重计算综合得分
        - **策略建议生成** - AI智能生成策略建议
    """)
    
    ## 快速功能入口
    st.divider()
    st.subheader("🚀 快速入口")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("开始权重计算", use_container_width=True):
            st.session_state.selected = "层次分析法计算主观权重"
            st.rerun()
    
    with col2:
        if st.button("查看综合评估", use_container_width=True):
            st.session_state.selected = "综合得分评估"
            st.rerun()
    
    with col3:
        if st.button("生成策略建议", use_container_width=True):
            st.session_state.selected = "策略建议生成"
            st.rerun()

elif selected == "层次分析法计算主观权重":
    st.title("层次分析法(AHP)计算主观权重")
    st.write("这里放置AHP权重计算的功能...")
    # 这里可以添加AHP计算的具体代码

elif selected == "熵权法计算客观权重":
    st.title("熵权法计算客观权重")
    st.write("这里放置熵权法计算的功能...")
    # 这里可以添加熵权法计算的具体代码

elif selected == "组合权重计算":
    st.title("组合权重计算")
    st.write("这里放置组合权重计算的功能...")
    # 这里可以添加组合权重计算的具体代码

elif selected == "综合得分评估":
    st.title("综合得分评估")
    st.write("这里放置综合得分评估的功能...")
    # 这里可以添加综合得分评估的具体代码

elif selected == "策略建议生成":
    st.title("AI策略建议生成")
    st.write("这里放置AI策略生成的功能...")
    # 这里可以添加AI策略生成的具体代码

## 页脚
st.divider()
st.caption("© 2025 生态增值，农策共荣 - 所有权利保留")