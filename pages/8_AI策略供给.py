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
    .streaming-text {
        line-height: 1.8;
        font-size: 16px;
        white-space: pre-wrap;
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
        
        # 根据API文档构建正确的请求体
        data = {
            "inputs": inputs,
            "query": "请基于提供的农业信息进行专业的生态产业分析和发展策略规划",  # 必需的query字段
            "response_mode": "streaming",  # 使用流式模式
            "user": user_id,
            "auto_generate_name": False  # 可选参数
        }
        
        # 如果有会话ID，添加到请求中
        if st.session_state.get('conversation_id'):
            data["conversation_id"] = st.session_state.conversation_id
        
        st.write("🔍 调试信息 - 请求数据:")
        st.json(data)
        
        try:
            response = requests.post(
                url, 
                headers=self.headers, 
                json=data, 
                stream=True, 
                timeout=60
            )
            
            st.write(f"🔍 响应状态码: {response.status_code}")
            
            if response.status_code != 200:
                error_detail = response.text
                st.error(f"❌ API返回错误: {response.status_code} - {error_detail}")
                yield f"API请求失败: {response.status_code} - {error_detail}", None
                return
            
            full_response = ""
            conversation_id = None
            
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    if line.startswith('data: '):
                        try:
                            event_data = json.loads(line[6:])  # 去掉 'data: ' 前缀
                            event_type = event_data.get('event')
                            
                            st.write(f"🔍 收到事件: {event_type}")
                            
                            if event_type == 'message' and 'answer' in event_data:
                                chunk = event_data['answer']
                                full_response += chunk
                                # 更新会话ID
                                if 'conversation_id' in event_data:
                                    conversation_id = event_data['conversation_id']
                                yield chunk, conversation_id
                                
                            elif event_type == 'message_end':
                                st.success("✅ 分析完成！")
                                if 'conversation_id' in event_data:
                                    conversation_id = event_data['conversation_id']
                                break
                                
                            elif event_type == 'error':
                                error_msg = event_data.get('message', '未知错误')
                                st.error(f"❌ 流式处理错误: {error_msg}")
                                yield f"错误: {error_msg}", None
                                break
                                
                        except json.JSONDecodeError as e:
                            st.warning(f"⚠️ JSON解析错误: {e}")
                            continue
                        except Exception as e:
                            st.error(f"❌ 处理事件时出错: {e}")
                            continue
            
            # 返回最终结果
            if full_response:
                yield full_response, conversation_id
            else:
                yield "未收到有效响应，请检查API配置。", None
                
        except requests.exceptions.RequestException as e:
            error_msg = f"❌ 请求失败: {str(e)}"
            st.error(error_msg)
            yield error_msg, None

# 初始化应用
def init_app():
    # 在这里配置您的API密钥
    API_KEY = "app-EL6JUFtLyHKzBCv1ASFRQZNe"  # 请替换为您的实际API密钥
    
    if not API_KEY or API_KEY == "your-api-key-here":
        st.error("⚠️ 请先配置API密钥")
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
        if submitted:
            if not province or not city or not agri_type:
                st.warning("⚠️ 请填写省份、城市和农业类型等必填信息")
            else:
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
                
                # 准备输入数据 - 确保变量名与提示词模板一致
                inputs = {
                    "province": province,
                    "city": city,
                    "village": village if village else "",
                    "agri_type": agri_type,
                    "production_scale": production_scale,
                    "special_prod": special_prod if special_prod else ""
                }
                
                # 检查API是否初始化
                if st.session_state.analyst is None:
                    st.error("❌ API未正确初始化，请检查API密钥配置")
                    return
                
                # 执行分析
                with col2:
                    st.header("💡 分析结果")
                    analysis_placeholder = st.empty()
                    
                    with analysis_placeholder.container():
                        st.markdown("<div class='analysis-result'>", unsafe_allow_html=True)
                        
                        # 显示加载状态
                        status_placeholder = st.empty()
                        with status_placeholder:
                            st.info("🔍 正在连接AI分析服务...")
                        
                        # 调用API进行分析
                        analysis_text = ""
                        try:
                            for chunk, conv_id in st.session_state.analyst.send_analysis_request(inputs):
                                if chunk:
                                    analysis_text += chunk
                                    # 清除加载状态，显示实际内容
                                    status_placeholder.empty()
                                    st.markdown(f'<div class="streaming-text">{analysis_text}</div>', unsafe_allow_html=True)
                                
                                if conv_id and not st.session_state.conversation_id:
                                    st.session_state.conversation_id = conv_id
                                    st.sidebar.success(f"会话ID: {conv_id[:8]}...")
                            
                            # 保存分析结果到历史
                            if analysis_text and len(analysis_text) > 10:  # 确保有实际内容
                                analysis_record = {
                                    "inputs": inputs,
                                    "analysis": analysis_text,
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                    "conversation_id": st.session_state.conversation_id
                                }
                                st.session_state.analysis_history.append(analysis_record)
                                st.sidebar.success("✅ 分析已保存到历史记录")
                            
                        except Exception as e:
                            st.error(f"❌ 分析过程中出错: {str(e)}")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
    
    # 历史记录部分
    if st.session_state.analysis_history:
        st.markdown("---")
        st.header("📚 分析历史")
        
        for i, record in enumerate(reversed(st.session_state.analysis_history[-3:]), 1):
            with st.expander(f"分析记录 {i} - {record['timestamp']}"):
                st.write("**输入信息:**")
                st.json(record['inputs'])
                st.write("**分析结果:**")
                st.write(record['analysis'])
    
    # 使用说明和调试信息
    with st.sidebar:
        st.markdown("---")
        st.header("🔧 调试信息")
        if st.session_state.get('conversation_id'):
            st.write(f"会话ID: `{st.session_state.conversation_id}`")
        
        st.markdown("---")
        st.header("💡 使用说明")
        st.markdown("""
        1. **填写基本信息**: 选择省份、城市，填写农业相关信息
        2. **提交分析**: 点击"开始分析"按钮
        3. **查看结果**: 在右侧查看专业的生态产业发展策略
        
        ### 必需字段：
        - ✅ 省份
        - ✅ 城市  
        - ✅ 农业类型
        """)

if __name__ == "__main__":
    main()