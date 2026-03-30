import os
import sys
import importlib.util

# functions フォルダをパスに追加
FUNCTIONS_DIR = os.path.join(os.path.dirname(__file__), "functions")
sys.path.append(FUNCTIONS_DIR)

def load_modules():
    modules = {}
    for folder in os.listdir(FUNCTIONS_DIR):
        folder_path = os.path.join(FUNCTIONS_DIR, folder)
        main_file = os.path.join(folder_path, "main.py")
        if os.path.isdir(folder_path) and os.path.isfile(main_file):
            spec = importlib.util.spec_from_file_location(f"{folder}.main", main_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            modules[folder] = mod
    return modules

if __name__ == "__main__":
    modules = load_modules()
    print("ハブ起動！見つかったモジュール:", list(modules.keys()), flush=True)
    
    # 全モジュールの run() を順番に呼ぶ
    for name, mod in modules.items():
        if hasattr(mod, "run"):
            print(f"モジュール {name} 実行中...", flush=True)
            mod.run()
        else:
            print(f"モジュール {name} に run() がありません", flush=True)
