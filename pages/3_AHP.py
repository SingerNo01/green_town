import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="AHP层次分析法计算工具",
    page_icon="📊",
    layout="wide"
)

# 定义RI字典
RI_dict = {
    1: 0, 2: 0, 3: 0.52, 4: 0.89, 5: 1.12, 6: 1.26, 7: 1.36,
    8: 1.41, 9: 1.46, 10: 1.49, 11: 1.52, 12: 1.54, 13: 1.56,
    14: 1.58, 15: 1.59, 16: 1.5943, 17: 1.6064, 18: 1.6133,
    19: 1.6207, 20: 1.6292
}

def check_reciprocal(matrix):
    """检查矩阵是否为互反矩阵"""
    n = matrix.shape[0]
    for i in range(n):
        for j in range(i + 1, n):
            if not np.isclose(matrix[i, j], 1 / matrix[j, i], atol=1e-5):
                return False
    return True

def calculate_weights_geometric(matrix):
    """几何平均法计算权重"""
    n = matrix.shape[0]
    row_products = np.prod(matrix, axis=1)
    W = np.power(row_products, 1 / n)
    return W / np.sum(W)

def calculate_weights_arithmetic(matrix):
    """算术平均法计算权重"""
    col_sums = np.sum(matrix, axis=0)
    normalized = matrix / col_sums
    return np.mean(normalized, axis=1)

def calculate_consistency(matrix, weights):
    """计算一致性指标"""
    n = matrix.shape[0]
    AW = np.dot(matrix, weights)
    lambda_max = np.mean(AW / weights)
    CI = (lambda_max - n) / (n - 1)
    CR = CI / RI_dict[n]
    return lambda_max, CI, CR

def main():
    st.title("AHP层次分析法计算工具")
    st.markdown("""
    ### 使用说明
    1. 上传包含判断矩阵的Excel文件
    2. 选择工作表
    3. 选择计算方法
    4. 执行AHP计算
    5. 查看结果并下载
    """)
    
    # 初始化session state
    if 'matrix' not in st.session_state:
        st.session_state.matrix = None
    if 'weights' not in st.session_state:
        st.session_state.weights = None
    if 'lambda_max' not in st.session_state:
        st.session_state.lambda_max = None
    if 'consistency_ratio' not in st.session_state:
        st.session_state.consistency_ratio = None
    
    # 文件上传
    uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            # 读取Excel文件
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names
            
            if not sheet_names:
                st.warning("Excel文件中没有工作表！")
                return
            
            # 选择工作表
            selected_sheet = st.selectbox("选择工作表", sheet_names)
            
            # 读取数据
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=None)
            rows, cols = df.shape
            
            if rows != cols:
                st.error("判断矩阵必须是方阵！")
                return
            
            if rows > 10:
                if st.checkbox("矩阵大小超过10×10限制，是否继续使用前10×10部分？"):
                    df = df.iloc[:10, :10]
                else:
                    return
            
            st.session_state.matrix = df.values
            
            # 显示矩阵
            st.subheader("判断矩阵")
            st.dataframe(df.style.format("{:.4f}"))
            
            # 计算方法选择
            method = st.radio("计算方法", ["几何平均", "算术平均"], horizontal=True)
            
            # 执行计算按钮
            if st.button("执行AHP计算"):
                if st.session_state.matrix is None:
                    st.warning("没有可计算的数据！")
                    return
                
                matrix = np.array(st.session_state.matrix, dtype=np.float64)
                
                if not check_reciprocal(matrix):
                    st.warning("判断矩阵不是严格的互反矩阵！")
                    if not st.checkbox("继续计算？"):
                        return
                
                # 计算权重
                if method == "几何平均":
                    weights = calculate_weights_geometric(matrix)
                else:
                    weights = calculate_weights_arithmetic(matrix)
                
                st.session_state.weights = weights
                lambda_max, CI, CR = calculate_consistency(matrix, weights)
                st.session_state.lambda_max = lambda_max
                st.session_state.consistency_ratio = CR
                
                # 显示结果
                st.subheader("AHP权重计算结果")
                weights_df = pd.DataFrame({
                    "因素": [f"因素{i+1}" for i in range(len(weights))],
                    "权重": [f"{w:.5f}" for w in weights]
                })
                st.dataframe(weights_df)
                
                # 可视化权重
                st.bar_chart(weights_df.set_index("因素"))
                
                # 显示一致性检验结果
                st.subheader("一致性检验")
                consistency_df = pd.DataFrame({
                    "指标": ["最大特征根(λ_max)", "一致性指标(CI)", "随机一致性指标(RI)", "一致性比率(CR)"],
                    "值": [f"{lambda_max:.5f}", f"{CI:.5f}", f"{RI_dict[len(weights)]:.5f}", f"{CR:.5f}"]
                })
                st.dataframe(consistency_df)
                
                if CR < 0.1:
                    st.success("✅ 一致性检验通过 (CR < 0.1)")
                else:
                    st.error("⚠️ 一致性检验未通过 (CR ≥ 0.1)! 请重新调整判断矩阵")
                
                # 下载结果
                st.subheader("下载结果")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"AHP计算结果_{timestamp}.xlsx"
                
                # 创建Excel文件
                output = pd.ExcelWriter(output_filename, engine='openpyxl')
                pd.DataFrame(matrix).to_excel(output, sheet_name=f"原始矩阵_{selected_sheet[:25]}", index=False, 
                                      header=[f"因素{i+1}" for i in range(matrix.shape[1])])
                weights_df.to_excel(output, sheet_name="权重结果", index=False)
                consistency_df.to_excel(output, sheet_name="一致性检验", index=False)
                output.close()
                
                # 提供下载链接
                with open(output_filename, "rb") as f:
                    st.download_button(
                        label="下载结果",
                        data=f,
                        file_name=output_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                # 删除临时文件
                os.remove(output_filename)
        
        except Exception as e:
            st.error(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()