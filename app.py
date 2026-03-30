import os
import runpy

# functions フォルダ
FUNCTIONS_DIR = os.path.join(os.path.dirname(__file__), "functions")

# サブフォルダを自動取得
for folder in os.listdir(FUNCTIONS_DIR):
    folder_path = os.path.join(FUNCTIONS_DIR, folder)
    main_file = os.path.join(folder_path, "main.py")
    
    if os.path.isdir(folder_path) and os.path.isfile(main_file):
        print(f"=== モジュール {folder} 実行開始 ===", flush=True)
        runpy.run_path(main_file, run_name="__main__")
        print(f"=== モジュール {folder} 実行終了 ===\n", flush=True)
