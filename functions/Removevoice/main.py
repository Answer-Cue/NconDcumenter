import streamlit as st
import noisereduce as nr
import librosa
import soundfile as sf
from io import BytesIO
from spleeter.separator import Separator

st.header("音声ノイズ除去 & ボーカル分離モジュール")

# 音声アップロード
uploaded_file = st.file_uploader("音声ファイルをアップロード (.wav)", type=["wav"])

if uploaded_file is not None:
    # 音声読み込み
    y, sr = librosa.load(uploaded_file, sr=None)
    st.audio(uploaded_file, format='audio/wav', start_time=0)
    st.write("元音声を再生中…")

    # ノイズ除去
    st.write("ノイズ除去中…")
    reduced_noise = nr.reduce_noise(y=y, sr=sr)

    buffer_denoised = BytesIO()
    sf.write(buffer_denoised, reduced_noise, sr, format='WAV')
    buffer_denoised.seek(0)
    st.audio(buffer_denoised, format='audio/wav', start_time=0)
    st.write("ノイズ除去後の音声を再生中…")
    st.download_button("ノイズ除去音声ダウンロード", buffer_denoised, "denoised.wav", mime="audio/wav")

    # 音楽とボーカルの分離
    st.write("音楽とボーカルを分離中…少々お待ちください")
    separator = Separator('spleeter:2stems')  # vocals / accompaniment に分離
    separator.separate_to_file(uploaded_file, 'output')  # output フォルダに書き出し

    # Streamlit 用に読み込み
    vocals_path = 'output/' + uploaded_file.name.replace('.wav','') + '/vocals.wav'
    accompaniment_path = 'output/' + uploaded_file.name.replace('.wav','') + '/accompaniment.wav'

    # 再生・ダウンロード
    for label, path in [("ボーカルのみ", vocals_path), ("伴奏のみ", accompaniment_path)]:
        st.audio(path, format='audio/wav')
        with open(path, 'rb') as f:
            st.download_button(f"{label} ダウンロード", f, path, mime="audio/wav")
