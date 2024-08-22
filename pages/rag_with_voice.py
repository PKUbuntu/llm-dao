import streamlit as st
import torch
import torchaudio
import numpy as np


from agent.ollama_client import client, model_options
selected_model = st.sidebar.selectbox('选择一个模型', model_options)

from st_audiorec import st_audiorec
input_wav = st_audiorec()

# if wav_audio_data is not None:
#     st.audio(wav_audio_data, format='audio/wav')


st.write("# Voice Demo: " + str(selected_model))

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


from agent.sence_voice_model import model

if input_wav:
    resampler = torchaudio.transforms.Resample(44100, 16000)
    input_wav_t = torch.from_numpy(np.frombuffer(input_wav, np.int32)).to(torch.float32)
    input_wav = resampler(input_wav_t[None, :])[0, :].numpy()

    res = model.generate(
        input=input_wav,
        cache={},
        language="auto",
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )

    # st.write(res)
    prompt = res[0]['text']

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
