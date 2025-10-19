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
    initial_sidebar_state="collapsed"  # 隐藏侧边栏
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
        text-align: center;
    }
    .input-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border-left: 4px solid #2E8B57;
        margin-bottom: 2rem;
    }
    .analysis-section {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-top: 2rem;
        border: 1px solid #e0e0e0;
    }
    .streaming-text {
        line-height: 1.8;
        font-size: 16px;
        white-space: pre-wrap;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 5px;
        border-left: 4px solid #4CAF50;
    }
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
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
            "user": user_id,
            "auto_generate_name": False
        }
        
        if st.session_state.get('conversation_id'):
            data["conversation_id"] = st.session_state.conversation_id
        
        try:
            response = requests.post(
                url, 
                headers=self.headers, 
                json=data, 
                stream=True, 
                timeout=60
            )
            
            if response.status_code != 200:
                error_detail = response.text
                return f"❌ API返回错误: {response.status_code} - {error_detail}", None
            
            full_response = ""
            conversation_id = None
            
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    if line.startswith('data: '):
                        try:
                            event_data = json.loads(line[6:])
                            event_type = event_data.get('event')
                            
                            if event_type == 'message' and 'answer' in event_data:
                                chunk = event_data['answer']
                                full_response += chunk
                                if 'conversation_id' in event_data:
                                    conversation_id = event_data['conversation_id']
                                yield chunk, conversation_id
                                
                            elif event_type == 'message_end':
                                if 'conversation_id' in event_data:
                                    conversation_id = event_data['conversation_id']
                                break
                                
                            elif event_type == 'error':
                                error_msg = event_data.get('message', '未知错误')
                                yield f"错误: {error_msg}", None
                                break
                                
                        except json.JSONDecodeError:
                            continue
            
            if full_response:
                yield full_response, conversation_id
            else:
                yield "未收到有效响应，请检查API配置。", None
                
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ 请求失败: {str(e)}"
            yield error_msg, None

# 初始化应用
def init_app():
    API_KEY = "app-EL6JUFtLyHKzBCv1ASFRQZNe"  # 使用您提供的API密钥
    
    if not API_KEY:
        st.error("⚠️ API密钥未配置")
        return None
    
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
    
    # 输入表单 - 放在主页面
    st.markdown("<div class='form-container'>", unsafe_allow_html=True)
    st.header("📊 输入信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # 地理位置信息
        st.subheader("📍 地理位置")
        province = st.selectbox(
            "省份 *",
            ["", "北京市", "天津市", "河北省", "山西省", "内蒙古自治区", "辽宁省", "吉林省", "黑龙江省",
             "上海市", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省",
             "湖南省", "广东省", "广西壮族自治区", "海南省", "重庆市", "四川省", "贵州省", "云南省",
             "西藏自治区", "陕西省", "甘肃省", "青海省", "宁夏回族自治区", "新疆维吾尔自治区", "台湾省",
             "香港特别行政区", "澳门特别行政区"]
        )
        
        city = st.text_input("城市 *")
        village = st.text_input("县/区")
    
    with col2:
        # 农业信息
        st.subheader("🌾 农业信息")
        # 使用API要求的精确枚举值
        agri_type = st.selectbox(
            "农业类型 *",
            ["", "种植业", "畜牧业", "林业", "渔业", "混合农业"],
            help="请根据API要求选择正确的农业类型"
        )
        
        production_scale = st.selectbox(
            "生产规模",
            ["", "小规模（家庭农场）", "中等规模（合作社）", "大规模（企业化）", "产业化集群"]
        )
        
        special_prod = st.text_input("特色产品", placeholder="例如：有机大米、特色水果等")
    
    # 提交按钮
    submitted = st.button("🚀 开始分析", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # 显示输入信息概览
    if submitted:
        if not province or not city or not agri_type:
            st.error("⚠️ 请填写带 * 号的必填信息（省份、城市、农业类型）")
        else:
            # 显示输入信息
            st.markdown("<div class='input-section'>", unsafe_allow_html=True)
            st.header("📝 输入信息确认")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.subheader("📍 地理位置")
                st.write(f"**省份:** {province}")
                st.write(f"**城市:** {city}")
                st.write(f"**县/区:** {village if village else '未填写'}")
            
            with info_col2:
                st.subheader("🌾 农业信息")
                st.write(f"**农业类型:** {agri_type}")
                st.write(f"**生产规模:** {production_scale if production_scale else '未填写'}")
                st.write(f"**特色产品:** {special_prod if special_prod else '未填写'}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 准备输入数据 - 使用API要求的精确值
            inputs = {
                "province": province,
                "city": city,
                "village": village if village else "",
                "agri_type": agri_type,
                "production_scale": production_scale if production_scale else "",
                "special_prod": special_prod if special_prod else ""
            }
            
            # 检查API是否初始化
            if st.session_state.analyst is None:
                st.error("❌ API未正确初始化，请检查API密钥配置")
                return
            
            # 执行分析
            st.markdown("<div class='analysis-section'>", unsafe_allow_html=True)
            st.header("💡 分析结果")
            
            # 显示加载状态
            status_placeholder = st.empty()
            with status_placeholder:
                st.info("🔍 AI正在分析您的农业项目，请稍候...")
                progress_bar = st.progress(0)
                for i in range(100):
                    progress_bar.progress(i + 1)
                    time.sleep(0.02)
            
            # 调用API进行分析
            analysis_text = ""
            result_placeholder = st.empty()
            
            try:
                for chunk, conv_id in st.session_state.analyst.send_analysis_request(inputs):
                    if chunk:
                        analysis_text += chunk
                        # 清除加载状态，显示实际内容
                        status_placeholder.empty()
                        with result_placeholder.container():
                            st.markdown(f'<div class="streaming-text">{analysis_text}</div>', unsafe_allow_html=True)
                    
                    if conv_id and not st.session_state.conversation_id:
                        st.session_state.conversation_id = conv_id
                
                # 保存分析结果到历史
                if analysis_text and len(analysis_text) > 10:
                    analysis_record = {
                        "inputs": inputs,
                        "analysis": analysis_text,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "conversation_id": st.session_state.conversation_id
                    }
                    st.session_state.analysis_history.append(analysis_record)
                    st.success("✅ 分析完成并已保存到历史记录")
                
            except Exception as e:
                st.error(f"❌ 分析过程中出错: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    # 历史记录部分
    if st.session_state.analysis_history:
        st.markdown("---")
        st.header("📚 历史分析记录")
        
        for i, record in enumerate(reversed(st.session_state.analysis_history[-5:]), 1):
            with st.expander(f"分析记录 {i} - {record['timestamp']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("输入信息")
                    st.json(record['inputs'])
                
                with col2:
                    st.subheader("分析结果")
                    st.write(record['analysis'])
    
    # 底部控制按钮
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("🔄 开始新的分析", use_container_width=True):
            st.session_state.conversation_id = None
            st.rerun()

if __name__ == "__main__":
    main()