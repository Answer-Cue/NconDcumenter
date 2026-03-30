import streamlit as st
import os
import runpy

FUNCTIONS_DIR = "functions"

st.title("Streamlit ハブ画面")

# セッションステートで選択管理
if "current_module" not in st.session_state:
    st.session_state.current_module = None

# モジュール選択画面
if st.session_state.current_module is None:
    st.write("モジュールを選択してください：")
    for folder in os.listdir(FUNCTIONS_DIR):
        folder_path = os.path.join(FUNCTIONS_DIR, folder)
        main_file = os.path.join(folder_path, "main.py")
        if os.path.isdir(folder_path) and os.path.isfile(main_file):
            if st.button(f"{folder} を起動"):
                st.session_state.current_module = folder
                st.experimental_rerun = lambda: None  # dummyで上書き（もはや呼ばない）
                # 再描画のためには下で return する
                st.experimental_rerun_triggered = True

# モジュール画面
if st.session_state.current_module is not None:
    module_path = os.path.join(FUNCTIONS_DIR, st.session_state.current_module, "main.py")
    try:
        runpy.run_path(module_path, run_name="__main__")
    except Exception as e:
        st.error(f"{st.session_state.current_module} 実行中にエラー: {e}")
