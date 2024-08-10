# 使用 ST 做几个实验功能
# 1. 使用 LLM 的简单对话
# 2. 一个基于具体文档基本的 RAG 搜索
# 3. 使用 Tool Call 做一个外部搜索

import streamlit as st

st.set_page_config(
    page_title="LLM-Demo", page_icon="👋",
)


st.write("# Yes, LLM!")


st.sidebar.success("Select a demo above.")


st.markdown(
    "## 欢迎 to Streamlit 👋"
)
