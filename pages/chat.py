# 使用 streamlit 的默认的 chat message 组件

import streamlit as st
from agent.ollama_client import client, model_options

selected_model = st.sidebar.selectbox('选择一个模型', model_options)

st.write("# Chat Demo: " + str(selected_model))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def response_generator(stream):
    for chunk in stream:
        yield chunk['message']['content']

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # st.code(st.session_state.messages, "javascript")
    response = client.chat(model=str(selected_model),
                           messages=st.session_state.messages,
                           stream=True)

    stream_resp = None
    with st.chat_message("assistant"):
        # st.code(response, "javascript")
        stream_resp = st.write_stream(response_generator(response))

    st.session_state.messages.append({"role": "assistant", "content": stream_resp})
