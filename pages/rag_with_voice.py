import streamlit as st
import torch
import torchaudio
import numpy as np


from st_audiorec import st_audiorec


input_wav = st_audiorec()

# if wav_audio_data is not None:
#     st.audio(wav_audio_data, format='audio/wav')

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

    st.write(res)
