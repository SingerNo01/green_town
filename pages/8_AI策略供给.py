import streamlit as st
import requests
import json
import time
from typing import Dict, Any, Generator

# 页面配置
st.set_page_config(
    page_title="智能农业生态产业分析助手",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin-bottom: 1rem;
    }
    .analysis-result {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
</style>
""", unsafe_allow_html=True)

class AgriculturalAnalyst:
    def __init__(self, api_key: str, base_url: str = "http://119.45.173.154/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def send_analysis_request(self, inputs: Dict[str, Any], user_id: str = "agricultural_user") -> Generator:
        """发送农业分析请求"""
        url = f"{self.base_url}/chat-messages"
        
        data = {
            "inputs": inputs,
            "query": "请基于提供的农业信息进行专业的生态产业分析和发展策略规划",
            "response_mode": "streaming",
            "user": user_id
        }
        
        if "conversation_id" in st.session_state:
            data["conversation_id"] = st.session_state.conversation_id
        
        try:
            response = requests.post(url, headers=self.headers, json=data, stream=True, timeout=30)
            response.raise_for_status()
            
            full_response = ""
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            event_data = json.loads(line_str[6:])
                            event_type = event_data.get('event')
                            
                            if event_type == 'message' and 'answer' in event_data:
                                chunk = event_data['answer']
                                full_response += chunk
                                yield chunk, event_data.get('conversation_id')
                                
                            elif event_type == 'message_end':
                                if event_data.get('conversation_id') and not st.session_state.get('conversation_id'):
                                    st.session_state.conversation_id = event_data['conversation_id']
                                break
                                
                        except json.JSONDecodeError:
                            continue
            
        except requests.exceptions.RequestException as e:
            yield f"❌ 请求失败: {str(e)}", None

# 初始化应用
def init_app():
    # 配置API密钥（在实际使用中应该从环境变量或配置文件中读取）
    API_KEY = "app-EL6JUFtLyHKzBCv1ASFRQZNe"  # 请替换为您的实际API密钥
    
    return AgriculturalAnalyst(API_KEY)

# 主应用
def main():
    # 页面标题
    st.markdown("""
    <div class="main-header">
        <h1>🌱 智能农业生态产业分析助手</h1>
        <p>基于科学的评估方法和AI技术，为您的农业项目提供全方位的价值评估和发展策略</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 初始化会话状态
    if "analyst" not in st.session_state:
        st.session_state.analyst = init_app()
    
    if "analysis_history" not in st.session_state:
        st.session_state.analysis_history = []
    
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None
    
    # 侧边栏 - 输入表单
    with st.sidebar:
        st.header("📊 农业项目信息")
        
        with st.form("agricultural_info"):
            # 地理位置信息
            st.subheader("📍 地理位置")
            province = st.selectbox(
                "省份",
                ["", "北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省",
                 "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省",
                 "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省", "贵州省", "云南省",
                 "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", "台湾省",
                 "香港特别行政区", "澳门特别行政区"]
            )
            
            city = st.text_input("城市")
            village = st.text_input("县/区")
            
            st.subheader("🌾 农业信息")
            agri_type = st.selectbox(
                "农业类型",
                ["", "粮食作物", "经济作物", "蔬菜种植", "水果种植", "畜牧养殖", "水产养殖", 
                 "林业", "特色农业", "休闲农业", "有机农业", "设施农业"]
            )
            
            production_scale = st.selectbox(
                "生产规模",
                ["", "小规模（家庭农场）", "中等规模（合作社）", "大规模（企业化）", "产业化集群"]
            )
            
            special_prod = st.text_input("特色产品", placeholder="例如：有机大米、特色水果等")
            
            # 提交按钮
            submitted = st.form_submit_button("🚀 开始分析")
    
    # 主内容区
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 输入信息概览")
        if submitted and province and city:
            st.markdown(f"""
            <div class="input-section">
                <h4>📍 地理位置</h4>
                <p><strong>省份:</strong> {province}</p>
                <p><strong>城市:</strong> {city}</p>
                <p><strong>县/区:</strong> {village if village else '未填写'}</p>
                
                <h4>🌾 农业信息</h4>
                <p><strong>农业类型:</strong> {agri_type}</p>
                <p><strong>生产规模:</strong> {production_scale}</p>
                <p><strong>特色产品:</strong> {special_prod if special_prod else '未填写'}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 准备输入数据
            inputs = {
                "province": province,
                "city": city,
                "village": village,
                "agri_type": agri_type,
                "production_scale": production_scale,
                "special_prod": special_prod
            }
            
            # 执行分析
            with col2:
                st.header("💡 分析结果")
                analysis_placeholder = st.empty()
                
                with analysis_placeholder.container():
                    st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                    result_placeholder = st.empty()
                    full_analysis = ""
                    
                    # 显示加载动画
                    with result_placeholder:
                        st.write("🔍 正在分析农业生态产业发展策略...")
                        progress_bar = st.progress(0)
                        
                        for i in range(100):
                            progress_bar.progress(i + 1)
                            time.sleep(0.02)
                    
                    # 调用API进行分析
                    analysis_text = ""
                    for chunk, conv_id in st.session_state.analyst.send_analysis_request(inputs):
                        if chunk:
                            analysis_text += chunk
                            result_placeholder.markdown(f"<div style='line-height: 1.6;'>{analysis_text}</div>", unsafe_allow_html=True)
                        
                        if conv_id and not st.session_state.conversation_id:
                            st.session_state.conversation_id = conv_id
                    
                    # 保存分析结果到历史
                    if analysis_text:
                        analysis_record = {
                            "inputs": inputs,
                            "analysis": analysis_text,
                            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "conversation_id": st.session_state.conversation_id
                        }
                        st.session_state.analysis_history.append(analysis_record)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
        
        elif submitted:
            st.warning("⚠️ 请至少填写省份、城市和农业类型等必填信息")
    
    # 历史记录部分
    if st.session_state.analysis_history:
        st.markdown("---")
        st.header("📚 分析历史")
        
        for i, record in enumerate(reversed(st.session_state.analysis_history[-5:]), 1):
            with st.expander(f"分析记录 {i} - {record['timestamp']}"):
                st.write("**输入信息:**")
                st.json(record['inputs'])
                st.write("**分析结果:**")
                st.write(record['analysis'])
    
    # 使用说明
    with st.sidebar:
        st.markdown("---")
        st.header("💡 使用说明")
        st.markdown("""
        1. **填写基本信息**: 选择省份、城市，填写农业相关信息
        2. **提交分析**: 点击"开始分析"按钮
        3. **查看结果**: 在右侧查看专业的生态产业发展策略
        4. **历史记录**: 查看最近的分析记录
        
        ### 分析内容涵盖：
        - 🌍 生态适宜性分析
        - 💰 产业发展潜力评估  
        - 🚀 创新发展策略
        - 📈 市场前景预测
        - 🌱 可持续发展建议
        """)

if __name__ == "__main__":
    main()