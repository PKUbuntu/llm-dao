# 一个最简单的 rag

from llama_index.core.chat_engine.types import ChatMode
import streamlit as st

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, Settings

from agent.ollama_client import model_options

# 获取 data 目录下的文件名
import os
files = os.listdir('data')


selected_model = st.sidebar.selectbox('选择一个模型', model_options)
selected_file = st.sidebar.selectbox('选择一个文件', files)


with st.sidebar:
    st.write("参数设置")
    max_tokens = st.slider("最大 token 数", min_value=1, max_value=4096, value=100)
    temperature = st.slider("温度", min_value=0.0, max_value=1.0, value=0.5)
    top_p = st.slider("top_p", min_value=0.0, max_value=1.0, value=0.9)    


llama_host = "http://" +  os.getenv('OLLAMA_HOST', 'localhost:11434')

st.write("# RAG Demo: " + str(selected_model))

Settings.llm = Ollama(model=str(selected_model), base_url=llama_host, request_timeout=360.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest", base_url=llama_host)

documents = SimpleDirectoryReader(input_files=["data/" + str(selected_file)]).load_data()

# service_context = ServiceContext.from_defaults(chunk_size_limit=1000, 
#    llm=Settings.llm, embed_model=Settings.embed_model)

index = VectorStoreIndex.from_documents(documents) # , service_context=Settings)

tab1, tab2, tab3 = st.tabs(["Chat", "Document", "Embedding"])

with tab1:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

with tab2:
    st.write(documents)

with tab3:
    st.write(index.vector_store)


if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    chat_engine = index.as_chat_engine(
        chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT, streaming=True
    )
    response_stream = chat_engine.stream_chat(prompt)

    stream_resp = None
    with st.chat_message("assistant"):
        # st.code(response, "javascript")
        # stream_resp = st.write_stream(response_stream)
        # response_stream.print_response_stream()
        stream_resp = st.write_stream(response_stream.response_gen)

    st.session_state.messages.append({"role": "assistant", "content": stream_resp})
