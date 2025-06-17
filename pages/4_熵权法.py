import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="稳健熵权法计算工具",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("稳健熵权法计算工具")
    st.markdown("""
    ### 使用说明
    1. 上传包含指标数据的Excel文件
    2. 设置指标类型和参数
    3. 选择标准化方法和权重使用方式
    4. 执行计算
    5. 查看结果并下载
    """)

    # 初始化session state
    if 'original_df' not in st.session_state:
        st.session_state.original_df = None
    if 'standardized_df' not in st.session_state:
        st.session_state.standardized_df = None
    if 'weighted_df' not in st.session_state:
        st.session_state.weighted_df = None
    if 'result_df' not in st.session_state:
        st.session_state.result_df = None
    if 'topsis_df' not in st.session_state:
        st.session_state.topsis_df = None
    if 'indicator_types' not in st.session_state:
        st.session_state.indicator_types = []
    if 'optimal_ranges' not in st.session_state:
        st.session_state.optimal_ranges = []
    if 'non_negative_shift' not in st.session_state:
        st.session_state.non_negative_shift = 0.01
    if 'has_header' not in st.session_state:
        st.session_state.has_header = True

    # 文件上传
    uploaded_file = st.file_uploader("选择Excel文件", type=["xlsx", "xls", "csv"])

    if uploaded_file is not None:
        try:
            # 读取文件
            if uploaded_file.name.endswith('.csv'):
                st.session_state.has_header = st.checkbox("CSV文件包含表头", value=True)
                st.session_state.original_df = pd.read_csv(
                    uploaded_file, 
                    header=0 if st.session_state.has_header else None
                )
            else:
                st.session_state.has_header = st.checkbox("Excel文件包含表头", value=True)
                excel_file = pd.ExcelFile(uploaded_file)
                sheet_names = excel_file.sheet_names
                
                if len(sheet_names) > 1:
                    selected_sheet = st.selectbox("选择工作表", sheet_names)
                    st.session_state.original_df = pd.read_excel(
                        uploaded_file, 
                        sheet_name=selected_sheet,
                        header=0 if st.session_state.has_header else None
                    )
                else:
                    st.session_state.original_df = pd.read_excel(
                        uploaded_file, 
                        header=0 if st.session_state.has_header else None
                    )

            # 显示原始数据
            st.subheader("原始数据")
            st.dataframe(st.session_state.original_df)

            # 设置指标类型
            if st.session_state.has_header:
                setup_indicator_settings()

        except Exception as e:
            st.error(f"文件读取错误: {str(e)}")

    # 计算参数设置
    if st.session_state.original_df is not None:
        with st.expander("计算参数设置", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.session_state.method_var = st.radio(
                    "标准化方法",
                    ["极差法", "平方和"],
                    index=0,
                    horizontal=True
                )
            
            with col2:
                st.session_state.weight_usage_var = st.radio(
                    "权重使用",
                    ["标准化后", "距离计算", "两者都用"],
                    index=2,
                    horizontal=True
                )
            
            with col3:
                st.session_state.non_negative_shift = st.number_input(
                    "非负平移值",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.01,
                    step=0.01,
                    format="%.2f"
                )

        # 执行计算按钮
        if st.button("执行计算"):
            if not st.session_state.indicator_types:
                st.warning("请先设置指标类型！")
            else:
                try:
                    perform_entropy_calculation()
                    st.success("计算完成！")
                except Exception as e:
                    st.error(f"计算过程中发生错误: {str(e)}")

        # 显示计算结果
        if st.session_state.result_df is not None:
            display_results()

def setup_indicator_settings():
    """设置指标类型和参数"""
    st.subheader("指标类型设置")
    
    n_indicators = st.session_state.original_df.shape[1]
    col_names = list(st.session_state.original_df.columns)
    
    # 初始化指标类型和范围
    if not st.session_state.indicator_types:
        st.session_state.indicator_types = ["max"] * n_indicators
        st.session_state.optimal_ranges = [(None, None)] * n_indicators
    
    # 创建指标设置表格
    settings = []
    for i in range(n_indicators):
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.markdown(f"**{col_names[i]}**")
        
        with col2:
            indicator_type = st.selectbox(
                f"类型_{i}",
                ["max", "min", "range"],
                index=["max", "min", "range"].index(st.session_state.indicator_types[i]),
                key=f"type_{i}"
            )
            st.session_state.indicator_types[i] = indicator_type
        
        with col3:
            if indicator_type == "range":
                a = st.number_input(
                    "最小值(a)",
                    value=st.session_state.optimal_ranges[i][0] or 0.0,
                    key=f"a_{i}"
                )
            else:
                a = None
        
        with col4:
            if indicator_type == "range":
                b = st.number_input(
                    "最大值(b)",
                    value=st.session_state.optimal_ranges[i][1] or 1.0,
                    key=f"b_{i}"
                )
                if a is not None and b is not None and a > b:
                    st.warning("最小值不能大于最大值，已自动交换")
                    a, b = b, a
            else:
                b = None
        
        st.session_state.optimal_ranges[i] = (a, b)

def standardize_data(df):
    """标准化数据"""
    if df is None:
        return None

    standardized = df.copy()
    n, m = df.shape

    for j in range(m):
        col = df.iloc[:, j]
        indicator_type = st.session_state.indicator_types[j]
        a, b = st.session_state.optimal_ranges[j]

        try:
            if indicator_type == "max":  # 极大型指标
                min_val = col.min()
                max_val = col.max()
                if max_val == min_val:
                    standardized.iloc[:, j] = 1.0
                else:
                    standardized.iloc[:, j] = (col - min_val) / (max_val - min_val)

            elif indicator_type == "min":  # 极小型指标
                min_val = col.min()
                max_val = col.max()
                if max_val == min_val:
                    standardized.iloc[:, j] = 1.0
                else:
                    standardized.iloc[:, j] = (max_val - col) / (max_val - min_val)

            elif indicator_type == "range":  # 适度指标
                if a is None or b is None:
                    raise ValueError(f"指标 '{df.columns[j]}' 是适度指标，但未设置有效范围")

                min_val = col.min()
                max_val = col.max()
                denominator = max(a - min_val, max_val - b)

                if denominator == 0:
                    standardized.iloc[:, j] = 1.0
                else:
                    for i in range(n):
                        val = col.iloc[i]
                        if val < a:
                            standardized.iloc[i, j] = 1 - (a - val) / denominator
                        elif val > b:
                            standardized.iloc[i, j] = 1 - (val - b) / denominator
                        else:
                            standardized.iloc[i, j] = 1.0
        except Exception as e:
            raise ValueError(f"指标 '{df.columns[j]}' 标准化失败: {str(e)}")

    # 应用标准化方法
    method = st.session_state.method_var
    if method == "平方和":  # 平方和法
        for j in range(m):
            col = standardized.iloc[:, j]
            norm = np.sqrt(np.sum(col**2))
            if norm > 0:
                standardized.iloc[:, j] = col / norm

    # 非负平移处理
    min_val = standardized.min().min()
    if min_val <= 0:
        standardized += abs(min_val) + st.session_state.non_negative_shift  # 保证所有值大于0

    return standardized

def calculate_entropy_weights(df):
    """计算熵权法权重"""
    if df is None:
        return None

    n, m = df.shape
    P = df.copy()

    # 计算比重
    for j in range(m):
        col_sum = df.iloc[:, j].sum()
        if col_sum <= 0:
            raise ValueError(f"指标 '{df.columns[j]}' 的和为0或负数，无法计算")
        P.iloc[:, j] = df.iloc[:, j] / col_sum

    # 计算熵值
    E = np.zeros(m)
    ln_n = np.log(n)

    for j in range(m):
        entropy = 0
        for i in range(n):
            p = P.iloc[i, j]
            if p > 0:
                entropy -= p * np.log(p)
            else:
                entropy -= 0  # 当p=0时，定义p*ln(p)=0
        E[j] = entropy / ln_n

    # 计算差异系数
    G = 1 - E

    # 处理特殊情况：所有熵值都为1
    if np.allclose(G, 0):
        G = np.ones(m)  # 赋予相等权重
        st.warning("所有指标的熵值都为1，已自动分配相等权重")

    # 计算权重
    W = G / np.sum(G)

    # 创建结果DataFrame - 保持原始顺序
    result_df = pd.DataFrame({
        "指标": df.columns,
        "熵值": E,
        "差异系数": G,
        "权重": W
    })

    # 添加排名列但不改变原始顺序
    ranked_df = result_df.copy()
    ranked_df = ranked_df.sort_values(by="权重", ascending=False)
    ranked_df["排序"] = range(1, len(ranked_df)+1)

    # 将排名映射回原始顺序
    rank_dict = dict(zip(ranked_df["指标"], ranked_df["排序"]))
    result_df["排序"] = result_df["指标"].map(rank_dict)

    return result_df

def calculate_topsis(df, weights):
    """计算TOPSIS结果"""
    if df is None or weights is None:
        return None, None

    # 根据权重使用选项处理数据
    weight_usage = st.session_state.weight_usage_var
    n, m = df.shape

    # 创建加权矩阵
    weighted_matrix = df.copy()
    if weight_usage in ["标准化后", "两者都用"]:
        for j in range(m):
            weighted_matrix.iloc[:, j] = df.iloc[:, j] * weights[j]

    # 确定正负理想解
    positive_ideal = []
    negative_ideal = []

    for j in range(m):
        col = weighted_matrix.iloc[:, j] if weight_usage in ["标准化后", "两者都用"] else df.iloc[:, j]
        if st.session_state.indicator_types[j] == "min":
            positive_ideal.append(col.min())
            negative_ideal.append(col.max())
        else:  # max or range
            positive_ideal.append(col.max())
            negative_ideal.append(col.min())

    # 计算距离
    distance_positive = []
    distance_negative = []

    for i in range(n):
        row = weighted_matrix.iloc[i, :] if weight_usage in ["标准化后", "两者都用"] else df.iloc[i, :]

        # 计算加权欧氏距离
        if weight_usage in ["距离计算", "两者都用"]:
            sum_pos = 0
            sum_neg = 0
            for j in range(m):
                sum_pos += (weights[j] * (row.iloc[j] - positive_ideal[j])) ** 2
                sum_neg += (weights[j] * (row.iloc[j] - negative_ideal[j])) ** 2
            distance_positive.append(np.sqrt(sum_pos))
            distance_negative.append(np.sqrt(sum_neg))
        else:
            sum_pos = 0
            sum_neg = 0
            for j in range(m):
                sum_pos += (row.iloc[j] - positive_ideal[j]) ** 2
                sum_neg += (row.iloc[j] - negative_ideal[j]) ** 2
            distance_positive.append(np.sqrt(sum_pos))
            distance_negative.append(np.sqrt(sum_neg))

    # 计算接近度
    closeness = []
    for i in range(n):
        if distance_positive[i] + distance_negative[i] == 0:
            closeness.append(0)
        else:
            closeness.append(distance_negative[i] / (distance_positive[i] + distance_negative[i]))

    # 创建结果DataFrame - 保持原始顺序
    topsis_df = pd.DataFrame({
        "方案": [f"方案{i+1}" for i in range(n)],
        "正理想解距离": distance_positive,
        "负理想解距离": distance_negative,
        "接近度": closeness
    })

    # 添加排名列但不改变原始顺序
    ranked_topsis = topsis_df.copy()
    ranked_topsis = ranked_topsis.sort_values(by="接近度", ascending=False)
    ranked_topsis["排名"] = range(1, len(ranked_topsis)+1)

    # 将排名映射回原始顺序
    rank_dict = dict(zip(ranked_topsis["方案"], ranked_topsis["排名"]))
    topsis_df["排名"] = topsis_df["方案"].map(rank_dict)

    return topsis_df, weighted_matrix

def perform_entropy_calculation():
    """执行熵权法计算"""
    if st.session_state.original_df is None:
        raise ValueError("没有可计算的数据！")

    # 检查指标设置是否完成
    if not st.session_state.indicator_types:
        raise ValueError("请先设置指标类型！")

    # 标准化数据
    st.session_state.standardized_df = standardize_data(st.session_state.original_df)
    if st.session_state.standardized_df is None:
        raise ValueError("数据标准化失败！")

    # 计算熵权法权重
    st.session_state.result_df = calculate_entropy_weights(st.session_state.standardized_df)
    if st.session_state.result_df is None:
        raise ValueError("权重计算失败！")

    # 提取权重
    weights = st.session_state.result_df["权重"].values

    # 计算TOPSIS结果
    st.session_state.topsis_df, st.session_state.weighted_df = calculate_topsis(
        st.session_state.standardized_df, 
        weights
    )

def display_results():
    """显示计算结果"""
    tab1, tab2, tab3, tab4 = st.tabs([
        "熵权法结果", 
        "标准化矩阵", 
        "加权矩阵", 
        "TOPSIS结果"
    ])

    with tab1:
        st.dataframe(st.session_state.result_df)
        
        # 可视化权重
        st.subheader("权重分布")
        weights_df = st.session_state.result_df[["指标", "权重"]].set_index("指标")
        st.bar_chart(weights_df)

    with tab2:
        st.dataframe(st.session_state.standardized_df.style.format("{:.4f}"))

    with tab3:
        st.dataframe(st.session_state.weighted_df.style.format("{:.4f}"))

    with tab4:
        st.dataframe(st.session_state.topsis_df)
        
        # 可视化TOPSIS结果
        st.subheader("方案排名")
        topsis_rank = st.session_state.topsis_df[["方案", "接近度"]].set_index("方案")
        st.bar_chart(topsis_rank)

    # 下载结果
    st.subheader("下载结果")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"熵权TOPSIS结果_{timestamp}.xlsx"
    
    # 创建Excel文件
    output = pd.ExcelWriter(output_filename, engine='openpyxl')
    st.session_state.original_df.to_excel(output, sheet_name="原始数据", index=False)
    st.session_state.standardized_df.to_excel(output, sheet_name="标准化矩阵", index=False)
    st.session_state.weighted_df.to_excel(output, sheet_name="加权矩阵", index=False)
    st.session_state.result_df.to_excel(
        output, 
        sheet_name="熵权法结果", 
        index=False,
        columns=["指标", "熵值", "差异系数", "权重", "排序"]
    )
    st.session_state.topsis_df.to_excel(
        output, 
        sheet_name="TOPSIS结果", 
        index=False,
        columns=["方案", "正理想解距离", "负理想解距离", "接近度", "排名"]
    )
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