import json

def safe_load_json(filepath: str):
    """
    安全加载 JSON 文件，出错时返回空字典并打印提示。
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"[WARNING] File not found: {filepath}")
        return {}
    except json.JSONDecodeError as e:
        print(f"[WARNING] Invalid JSON in {filepath}: {e}")
        return {}