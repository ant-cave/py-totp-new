"""
测试密码流程
模拟设置密码和重新进入应用的过程
"""

import sys
import os
import time
from pathlib import Path

# 添加src目录到路径
sys.path.append('src')

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def test_password_flow():
    """测试密码流程"""
    print("=== 测试密码流程 ===")
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    # 初始状态检查
    print("初始状态:")
    print(f"  有现有密码: {totp_manager.has_existing_password()}")
    print(f"  数据文件存在: {(Path('data') / 'totp_data.json').exists()}")
    
    # 模拟设置密码
    print("\n1. 设置密码...")
    test_password = "test123"
    if totp_manager.initialize_with_password(test_password):
        print("  密码设置成功")
        
        # 添加一个测试条目
        print("2. 添加测试条目...")
        if totp_manager.add_entry("测试服务", "JBSWY3DPEHPK3PXP"):
            print("  测试条目添加成功")
        else:
            print("  测试条目添加失败")
    else:
        print("  密码设置失败")
        return
    
    # 检查设置后的状态
    print("\n设置密码后状态:")
    print(f"  有现有密码: {totp_manager.has_existing_password()}")
    print(f"  数据文件存在: {(Path('data') / 'totp_data.json').exists()}")
    print(f"  条目数量: {len(totp_manager.get_all_entries())}")
    
    # 模拟重新创建TOTP管理器（模拟重新启动应用）
    print("\n3. 模拟重新启动应用...")
    totp_manager2 = TOTPManager()
    
    print("重新启动后状态:")
    print(f"  有现有密码: {totp_manager2.has_existing_password()}")
    print(f"  数据文件存在: {(Path('data') / 'totp_data.json').exists()}")
    
    # 检查数据文件内容
    data_file = Path("data") / "totp_data.json"
    if data_file.exists():
        try:
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                entries = data.get("entries", [])
                print(f"  数据文件中的条目数量: {len(entries)}")
                if entries:
                    entry = entries[0]
                    print(f"  第一个条目有加密密钥: {'encrypted_key' in entry and entry['encrypted_key'] is not None}")
                    print(f"  第一个条目有盐值: {'salt' in entry and entry['salt'] is not None}")
        except Exception as e:
            print(f"  读取数据文件错误: {e}")
    
    print("\n=== 测试完成 ===")
    
    # 清理：删除测试数据文件
    if data_file.exists():
        data_file.unlink()
        print("已清理测试数据文件")

if __name__ == "__main__":
    test_password_flow()
