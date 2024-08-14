# rag + chromadb
import chromadb

from llama_index.core.chat_engine.types import ChatMode
import streamlit as st

from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext, VectorStoreIndex, Settings

import ollama
client = ollama.Client()

models = ollama.list()

model_options = []
for m in models['models']:
    model_options.append(m['model'])

# initialize client
db = chromadb.PersistentClient(path="./chroma_db")

index_names = []
cols = db.list_collections()
for c in cols:
    index_names.append(c.name)

selected_model = st.sidebar.selectbox('选择一个模型', model_options)
selected_file = st.sidebar.selectbox('选择一个向量索引', index_names)

# get index
chroma_collection = db.get_or_create_collection(str(selected_file))

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

import os
llama_host = "http://" +  os.getenv('OLLAMA_HOST', 'localhost:11434')

st.write("# RAG Demo: " + str(selected_model))

Settings.llm = Ollama(model=str(selected_model), base_url=llama_host, request_timeout=360.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest", base_url=llama_host)

index = VectorStoreIndex.from_vector_store(vector_store, 
                                           storage_context=storage_context)


chat_engine = index.as_chat_engine(
    chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT, streaming=True
)

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
    "Unknown"
    # st.write(index.ref_doc_info)

with tab3:
    st.write(index.vector_store)


if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response_stream = chat_engine.stream_chat(prompt)

    stream_resp = None
    with st.chat_message("assistant"):
        stream_resp = st.write_stream(response_stream.response_gen)

    st.session_state.messages.append({"role": "assistant", "content": stream_resp})
