import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

def main():
    st.set_page_config(
        page_title="组合权重计算工具",
        page_icon="⚖️",
        layout="wide"
    )

    st.title("组合权重计算工具(乘法合成)")
    st.markdown("""
    ### 使用说明
    1. 上传包含多种权重数据的Excel文件
    2. 选择工作表（如有多个）
    3. 执行组合权重计算
    4. 查看结果并下载
    """)

    # 初始化session state
    if 'weights_data' not in st.session_state:
        st.session_state.weights_data = None
    if 'result_df' not in st.session_state:
        st.session_state.result_df = None
    if 'combined_weights' not in st.session_state:
        st.session_state.combined_weights = None
    if 'num_weights' not in st.session_state:
        st.session_state.num_weights = 0
    if 'num_criteria' not in st.session_state:
        st.session_state.num_criteria = 0

    # 文件上传
    uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_names = excel_file.sheet_names

            if len(sheet_names) > 1:
                selected_sheet = st.selectbox("选择工作表", sheet_names)
                df = pd.read_excel(uploaded_file, sheet_name=selected_sheet, header=0)
            else:
                df = pd.read_excel(uploaded_file, header=0)

            if df.shape[1] < 2:
                st.error("数据格式错误: 至少需要两列权重数据!")
                return

            weight_cols = [col for col in df.columns if '权重' in str(col)]
            if not weight_cols:
                st.error("数据格式错误: 没有找到包含'权重'的列!")
                return

            st.session_state.weights_data = df[weight_cols].values
            st.session_state.num_weights = len(weight_cols)
            st.session_state.num_criteria = df.shape[0]

            # 显示原始数据
            st.subheader("权重数据")
            st.dataframe(df.style.format({col: "{:.5f}" for col in weight_cols}))

        except Exception as e:
            st.error(f"文件读取错误: {str(e)}")

    # 执行计算按钮
    if st.button("执行组合权重计算"):
        if st.session_state.weights_data is None:
            st.warning("没有可计算的数据！")
        else:
            try:
                if np.any(st.session_state.weights_data <= 0):
                    raise ValueError("权重数据必须全部为正数!")

                # 乘法合成法计算组合权重
                product_weights = np.prod(st.session_state.weights_data, axis=1)
                combined_weights = product_weights / np.sum(product_weights)
                st.session_state.combined_weights = combined_weights

                # 创建结果DataFrame
                results = {
                    "指标": [f"指标{i + 1}" for i in range(st.session_state.num_criteria)],
                    **{f"权重方法{i + 1}": [f"{w:.5f}" for w in st.session_state.weights_data[:, i]]
                        for i in range(st.session_state.num_weights)},
                    "组合权重": [f"{w:.5f}" for w in combined_weights]
                }
                st.session_state.result_df = pd.DataFrame(results)

                st.success("计算完成！")

                # 显示计算结果
                st.subheader("组合权重计算结果")
                st.dataframe(st.session_state.result_df)

                # 验证权重和
                sum_weights = np.sum(combined_weights)
                if np.isclose(sum_weights, 1.0, atol=1e-5):
                    st.success(f"权重和验证通过: {sum_weights:.5f}")
                else:
                    st.warning(f"⚠️ 权重和不为1: {sum_weights:.5f}")

            except Exception as e:
                st.error(f"计算过程中发生错误: {str(e)}")

    # 下载结果
    if st.session_state.result_df is not None:
        st.subheader("下载结果")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"组合权重结果_{timestamp}.xlsx"
        
        # 创建Excel文件
        output = pd.ExcelWriter(output_filename, engine='openpyxl')
        st.session_state.result_df.to_excel(output, sheet_name="组合权重结果", index=False)
        
        # 添加计算摘要
        summary_data = {
            "信息": ["权重方法数量", "指标数量", "计算时间"],
            "值": [
                st.session_state.num_weights, 
                st.session_state.num_criteria, 
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
        }
        pd.DataFrame(summary_data).to_excel(output, sheet_name="计算摘要", index=False)
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

if __name__ == "__main__":
    main()