import streamlit as st
import noisereduce as nr
import librosa
import soundfile as sf
from io import BytesIO

st.header("音声ノイズ除去モジュール（Cloud 安定版）")

uploaded_file = st.file_uploader("音声ファイルをアップロード (.wav)", type=["wav"])

if uploaded_file is not None:
    # 音声読み込み
    y, sr = librosa.load(uploaded_file, sr=None)
    st.audio(uploaded_file, format='audio/wav', start_time=0)
    st.write("元音声を再生中…")

    # ノイズ除去
    st.write("ノイズ除去中…少々お待ちください")
    reduced_noise = nr.reduce_noise(y=y, sr=sr)

    # 処理後音声を BytesIO に保存
    buffer = BytesIO()
    sf.write(buffer, reduced_noise, sr, format='WAV')
    buffer.seek(0)

    st.audio(buffer, format='audio/wav', start_time=0)
    st.write("ノイズ除去後の音声を再生中…")

    # ダウンロードリンク
    st.download_button(
        label="ノイズ除去後の音声をダウンロード",
        data=buffer,
        file_name="denoised.wav",
        mime="audio/wav"
    )
