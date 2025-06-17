import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

def main():
    st.set_page_config(
        page_title="综合评分计算工具",
        page_icon="📊",
        layout="wide"
    )

    st.title("综合评分计算工具")
    st.markdown("""
    ### 使用说明
    1. 上传包含组合权重和标准化数据的Excel文件（格式：第一列权重，第三列指标名称，第四列开始数据）
    2. 执行综合评分计算
    3. 下载结果文件（将生成与示例完全相同的格式）
    """)

    # 初始化session state
    if 'final_result' not in st.session_state:
        st.session_state.final_result = None

    # 文件上传
    uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            # 读取Excel文件
            df = pd.read_excel(uploaded_file, header=None)
            
            # 解析数据
            weights = df.iloc[1:, 0].astype(float).values
            indicator_names = df.iloc[1:, 2].values
            standardized_data = df.iloc[1:, 3:].astype(float)
            standardized_data.columns = [f"指标{i+1}" for i in range(standardized_data.shape[1])]
            standardized_data.index = indicator_names
            
            # 显示数据预览
            st.subheader("数据预览")
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("组合权重")
                weights_df = pd.DataFrame({
                    "指标名称": indicator_names,
                    "组合权重": weights
                })
                st.dataframe(weights_df.style.format({"组合权重": "{:.6f}"}))
            
            with col2:
                st.write("标准化数据矩阵 (前5行)")
                st.dataframe(standardized_data.head().style.format("{:.6f}"))

            # 执行计算按钮
            if st.button("执行综合评分计算"):
                # 归一化权重
                normalized_weights = weights / np.sum(weights)
                
                # 计算加权矩阵
                weighted_matrix = standardized_data.multiply(normalized_weights, axis=0)
                weighted_matrix.columns = [f"方案{i+1}" for i in range(weighted_matrix.shape[1])]
                
                # 计算综合得分
                scores = weighted_matrix.sum(axis=0)
                
                # 创建结果DataFrame
                result_df = pd.DataFrame({
                    "方案": weighted_matrix.columns,
                    "综合得分": scores.values,
                    "排名": scores.rank(ascending=False).astype(int).values
                }).sort_values("排名")
                
                # 准备最终输出格式
                final_output = {
                    "组合权重": weights_df,
                    "标准化矩阵": standardized_data,
                    "加权矩阵": weighted_matrix,
                    "综合评价结果": result_df
                }
                
                st.session_state.final_result = final_output
                st.success("计算完成！")
                
                # 显示计算结果
                st.subheader("综合评价结果")
                st.dataframe(result_df.style.format({"综合得分": "{:.6f}"}))
                
                # 可视化结果
                st.subheader("综合得分分布")
                st.bar_chart(result_df.set_index("方案")["综合得分"])

        except Exception as e:
            st.error(f"文件处理错误: {str(e)}")
            st.error("请确保文件格式正确：第一列权重，第三列指标名称，第四列开始是标准化数据")

    # 下载结果
    if st.session_state.final_result is not None:
        st.subheader("生成结果文件")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"综合得分_综合评价结果_{timestamp}.xlsx"
        
        # 创建Excel文件（完全按照要求的格式）
        with pd.ExcelWriter(output_filename, engine='openpyxl') as writer:
            # 1. 组合权重表
            st.session_state.final_result["组合权重"].to_excel(
                writer,
                sheet_name="组合权重",
                index=False,
                header=["指标名称", "组合权重"]
            )
            
            # 2. 标准化矩阵表
            standardized_df = st.session_state.final_result["标准化矩阵"].copy()
            standardized_df.reset_index(inplace=True)
            standardized_df.columns = ["指标名称"] + [f"指标{i+1}" for i in range(standardized_df.shape[1]-1)]
            standardized_df.to_excel(
                writer,
                sheet_name="标准化矩阵",
                index=False
            )
            
            # 3. 加权矩阵表（特殊格式）
            weighted_df = st.session_state.final_result["加权矩阵"].copy()
            weighted_df.reset_index(inplace=True)
            
            # 创建符合要求的加权矩阵格式
            weighted_output = pd.DataFrame()
            weighted_output["方案"] = ["指标"+str(i+1) for i in range(weighted_df.shape[0])]
            
            for col in weighted_df.columns[1:]:
                weighted_output[col] = weighted_df[col]
            
            weighted_output.to_excel(
                writer,
                sheet_name="加权矩阵",
                index=False
            )
            
            # 4. 综合评价结果表
            st.session_state.final_result["综合评价结果"].to_excel(
                writer,
                sheet_name="综合评价结果",
                index=False,
                columns=["方案", "综合得分", "排名"]
            )
        
        # 提供下载链接
        with open(output_filename, "rb") as f:
            st.download_button(
                label="下载结果文件",
                data=f,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="下载的文件将完全符合示例格式要求"
            )
        
        # 显示文件生成信息
        st.info("文件包含4个工作表：组合权重、标准化矩阵、加权矩阵、综合评价结果")

if __name__ == "__main__":
    main()