"""
调试当前系统状态
检查密码检测和验证逻辑
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
sys.path.append('src')

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def debug_current_state():
    """调试当前系统状态"""
    print("=== 调试当前系统状态 ===")
    
    # 检查数据目录和文件
    data_dir = Path("data")
    data_file = data_dir / "totp_data.json"
    
    print(f"数据目录存在: {data_dir.exists()}")
    print(f"数据文件存在: {data_file.exists()}")
    
    # 检查加密管理器状态
    encryption = EncryptionManager()
    print(f"加密系统已初始化: {encryption.is_initialized()}")
    print(f"存在加密数据: {encryption.has_encrypted_data()}")
    
    # 检查TOTP管理器状态
    totp_manager = TOTPManager()
    print(f"TOTP管理器有现有密码: {totp_manager.has_existing_password()}")
    
    # 如果数据文件存在，检查内容
    if data_file.exists():
        try:
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"数据文件内容: {data}")
                entries = data.get("entries", [])
                print(f"条目数量: {len(entries)}")
                if entries:
                    print(f"第一个条目: {entries[0]}")
        except Exception as e:
            print(f"读取数据文件错误: {e}")
    
    print("=== 调试完成 ===")

if __name__ == "__main__":
    debug_current_state()
