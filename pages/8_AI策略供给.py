import streamlit as st
import requests
import json
import time

st.title("生态产业策略分析系统")

# 自定义CSS
st.markdown("""
<style>
    .stSelectbox, .stTextInput, .stTextArea {
        margin-bottom: 1rem;
    }
    
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
    
    .analysis-result {
        background-color: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 在这里添加您的DeepSeek API密钥
DEEPSEEK_API_KEY = "sk-75937a540248461983ea1fd41c665405"  # ← 请在这里替换为您的API密钥

# 初始化session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False

# DeepSeek API配置
def call_deepseek_api(prompt):
    """
    调用DeepSeek API
    """
    url = "https://api.deepseek.com/v1/chat/"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是一位专业的农业生态产业分析师，擅长为不同地区的农业项目提供专业的生态产业发展策略。请提供具体、可操作的建议。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['choices'][0]['message']['content']
        
    except requests.exceptions.RequestException as e:
        return f"API调用错误: {str(e)}"
    except KeyError:
        return "API响应格式错误，请检查API密钥和请求参数"
    except Exception as e:
        return f"发生未知错误: {str(e)}"

# 创建两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.header("🏡 农业信息收集")
    
    # 地区选择
    province = st.selectbox(
        "省份:",
        ["北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省", 
         "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", 
         "湖北省", "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省", 
         "贵州省", "云南省", "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", 
         "新疆维吾尔自治区"],
        key="province"
    )
    
    city = st.text_input("城市:", key="city", placeholder="例如：石家庄市")
    village = st.text_input("区/县:", key="village", placeholder="例如：平山县")
    
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
        placeholder="例如：\n优质水稻\n有机蔬菜\n特色水果",
        key="special_prod"
    )
    
    # 额外信息
    additional_info = st.text_area(
        "其他相关信息(可选):",
        placeholder="例如：\n- 现有资源情况\n- 市场需求\n- 技术条件\n- 资金状况",
        key="additional_info"
    )
    
    # 生成分析按钮
    analyze_button = st.button("生成策略分析", type="primary")

with col2:
    st.header("🤖 AI策略分析")
    
    if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        st.error("⚠️ 请先配置API密钥")
        st.info("""
        **配置方法：**
        在代码中找到 `DEEPSEEK_API_KEY` 变量，将 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 
        替换为您实际的DeepSeek API密钥
        """)
    
    elif analyze_button:
        if not all([province, city, village, agri_type, production_scale]):
            st.error("请填写所有必填字段")
        else:
            # 构造发送给AI的提示语
            prompt = f"""
请基于以下农业信息提供详细的生态产业发展策略：

## 基本信息
- **地理位置**：{province}{city}{village}
- **农业类型**：{agri_type}
- **生产规模**：{production_scale}
- **特色产品**：{special_prod if special_prod else "暂无明确特色产品"}
- **其他信息**：{additional_info if additional_info else "无"}

## 分析要求
请从以下方面提供专业、具体的建议：

### 1. 生态农业发展模式
- 最适合该地区的生态农业模式
- 具体实施步骤和技术路线
- 生态效益评估

### 2. 产业优化策略
- 生产规模优化建议
- 产业链延伸方向
- 资源循环利用方案

### 3. 市场与营销
- 特色产品市场定位
- 品牌建设策略
- 销售渠道建议

### 4. 政策与资金
- 可申请的政策支持
- 补贴方向和申请条件
- 融资渠道建议

### 5. 风险评估
- 主要风险因素分析
- 风险防范措施
- 应急预案建议

请提供具体、可操作的建议，避免泛泛而谈。
"""
            
            # 显示加载状态
            st.session_state.is_loading = True
            with st.spinner("🤖 AI正在分析中，请稍候..."):
                # 调用API
                result = call_deepseek_api(prompt)
                st.session_state.analysis_result = result
                st.session_state.is_loading = False
            
            # 显示结果
            if st.session_state.analysis_result:
                if "错误" in st.session_state.analysis_result:
                    st.error(st.session_state.analysis_result)
                else:
                    st.success("✅ 分析完成！")
                    st.markdown("### 分析结果")
                    st.markdown(f'<div class="analysis-result">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
                    
                    # 添加下载功能
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    filename = f"生态产业策略分析_{timestamp}.txt"
                    
                    st.download_button(
                        label="📥 下载分析报告",
                        data=st.session_state.analysis_result,
                        file_name=filename,
                        mime="text/plain"
                    )
    
    # 显示历史结果
    elif st.session_state.analysis_result and not st.session_state.is_loading:
        st.markdown("### 分析结果")
        st.markdown(f'<div class="analysis-result">{st.session_state.analysis_result}</div>', unsafe_allow_html=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"生态产业策略分析_{timestamp}.txt"
        
        st.download_button(
            label="📥 下载分析报告",
            data=st.session_state.analysis_result,
            file_name=filename,
            mime="text/plain"
        )

# 侧边栏说明
with st.sidebar:
    st.header("使用说明")
    st.markdown("""
    ### 📝 使用步骤：
    1. **填写农业信息**
       - 选择或输入地区信息
       - 选择农业类型和规模
       - 描述特色产品
    
    2. **生成分析**
       - 点击"生成策略分析"按钮
       - 等待AI分析完成
       - 查看并下载分析报告
    
    ### 💡 提示：
    - 信息越详细，分析结果越精准
    - 可以在"其他信息"中补充更多背景
    - 支持下载分析报告保存
    """)
    
    st.header("支持的功能")
    st.markdown("""
    - ✅ 生态农业模式推荐
    - ✅ 产业优化策略
    - ✅ 市场定位分析
    - ✅ 政策支持指导
    - ✅ 风险评估预警
    - ✅ 报告下载保存
    """)