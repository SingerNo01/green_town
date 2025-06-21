# app.py
import streamlit as st
import os
import zipfile
from io import BytesIO

## 设置页面配置
st.set_page_config(
    page_title="生态增值，收集共荣",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

## 主标题
st.title("生态增值，收集共荣")
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

# EXE文件下载部分
st.header("应用程序下载")

# 分卷文件列表
part_files = [
    "绿野丰荣安装包.zip.001",
    "绿野丰荣安装包.zip.002",
    "绿野丰荣安装包.zip.003",
    "绿野丰荣安装包.zip.004"
]

def create_combined_zip():
    # 检查文件是否存在
    missing_files = [f for f in part_files if not os.path.exists(f)]
    if missing_files:
        st.error(f"缺少分卷文件: {', '.join(missing_files)}")
        return None
    
    # 创建内存中的ZIP文件
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for part in part_files:
            zipf.write(part, os.path.basename(part))
    
    zip_buffer.seek(0)  # 重置指针位置
    return zip_buffer

# 创建并下载组合ZIP
zip_buffer = create_combined_zip()
if zip_buffer:
    st.download_button(
        label="一键下载完整安装包",
        data=zip_buffer,
        file_name="绿野丰荣_完整安装包.zip",
        mime="application/zip",
        help="包含所有分卷的压缩包，下载后解压即可"
    )
    
    # 添加使用说明
    st.markdown("""
    ### 使用说明：
    1. 点击上方按钮下载完整安装包
    2. 下载完成后解压ZIP文件
    3. 解压后会得到4个分卷文件
    4. **只需解压第一个分卷**（绿野丰荣安装包.zip.001）
    5. 系统会自动合并所有分卷完成安装
    """)

## 页脚
st.divider()
st.caption("© 2025 生态增值，收集共享 - 所有权限保留")
