import streamlit as st

st.title("生态产业策略分析系统")

# 自定义CSS（添加iframe样式）
st.markdown("""
<style>
    /* 表单元素样式 */
    .stSelectbox, .stTextInput, .stTextArea {
        margin-bottom: 1rem;
    }
    
    /* 按钮样式 */
    .stButton>button {
        width: 100%;
        padding: 0.5rem;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    /* iframe容器样式 */
    .iframe-container {
        height: 75vh;  /* 视窗高度的75% */
        width: 100%;
        border: 1px solid #ddd;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* iframe本身样式 */
    .iframe-container iframe {
        width: 100%;
        height: 100%;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# 创建两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🏡 农业信息收集")
    
    # 地区选择 - 三级结构
    province = st.selectbox(
        "省份:",
        ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", 
         "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", 
         "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省", 
         "贵州省", "云南省", "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", 
         "新疆维吾尔自治区"],
        key="province"
    )
    
    city = st.text_input("城市:", key="city")
    village = st.text_input("区/县:", key="village")
    
    # 农业信息
    agri_type = st.selectbox(
        "农业类型:",
        ["种植业", "畜牧业", "林业", "渔业", "混合农业"],
        key="agri_type"
    )
    
    production_scale = st.selectbox(
        "生产规模:",
        ["小规模(家庭农场)", "中等规模(合作社)", "大规模(农业企业)"],
        key="production_scale"
    )
    
    special_prod = st.text_area(
        "特色产品(每行一个):",
        "产品1\n产品2\n产品3",
        key="special_prod"
    )
    
    # 生成分析按钮
    if st.button("生成策略分析", type="primary"):
        # 构造发送给AI的提示语
        prompt = f"""
        请基于以下农业信息提供生态产业发展策略：
        
        地理位置：{province}{city}{village}
        农业类型：{agri_type}
        生产规模：{production_scale}
        特色产品：{special_prod}
        
        请提供以下方面的专业建议：
        1. 适合该地区的生态农业发展模式
        2. 特色产品的市场定位和营销策略
        3. 生产规模优化建议
        4. 可能的政策支持和补贴方向
        5. 风险评估和应对措施
        """
        
        # 存储生成的提示语
        st.session_state.generated_prompt = prompt
        st.success("请在右侧聊天窗口粘贴以下内容获取专业分析：")
        st.code(prompt)
        
        # 提示用户可以直接拖拽表格到聊天窗口
        st.info("提示：您可以将综合评价表格直接拖拽到右侧DeepSeek聊天窗口进行分析")

with col2:
    st.header("🤖 DeepSeek 策略分析")
    
    # 添加跳转按钮（顶部提示）
    st.markdown("""
    <div style="background-color: #fff3cd; padding: 10px; border-radius: 5px; margin-bottom: 15px; border: 1px solid #ffeeba;">
    <b>⚠️ 如果无法显示聊天窗口：</b><br>
    <a href="https://chat.deepseek.com" target="_blank" style="background-color: #4CAF50; color: white; padding: 8px 16px; text-align: center; text-decoration: none; display: inline-block; border-radius: 4px; margin-top: 8px;">点此跳转至DeepSeek官网</a>
    </div>
    """, unsafe_allow_html=True)
    
    # 使用自定义iframe容器
    st.markdown("""
    <div class="iframe-container">
        <iframe src="https://chat.deepseek.com/embed"></iframe>
    </div>
    """, unsafe_allow_html=True)
    
    if 'generated_prompt' in st.session_state:
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin-top: 10px;">
        <b>操作指南:</b><br>
        1. 复制左侧生成的提示语<br>
        2. 粘贴到右侧聊天窗口（或官网页面）<br>
        3. 如需分析表格，可直接拖拽文件到聊天窗口<br><br>
        
        <span style="color: #d35400;">如果上方窗口无法使用：</span><br>
        • 点击本页面顶部按钮跳转至官网<br>
        • 在官网粘贴相同内容即可获得分析
        </div>
        """, unsafe_allow_html=True)
