#!/usr/bin/env python3
"""
测试密码检测功能
验证应用能够正确区分首次使用和已有密码的情况
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def test_password_detection():
    """测试密码检测功能"""
    print("=== 测试密码检测功能 ===")
    
    # 创建加密管理器实例
    encryption = EncryptionManager()
    
    # 创建TOTP管理器实例
    totp_manager = TOTPManager()
    
    print("1. 检查是否存在加密数据...")
    has_encrypted = encryption.has_encrypted_data()
    print(f"   存在加密数据: {has_encrypted}")
    
    print("2. 检查是否已有密码...")
    has_password = totp_manager.has_existing_password()
    print(f"   已有密码: {has_password}")
    
    print("3. 检查数据目录状态...")
    data_dir = "data"
    if os.path.exists(data_dir):
        print(f"   数据目录存在: {data_dir}")
        files = os.listdir(data_dir)
        print(f"   数据文件: {files}")
        
        # 检查 totp_data.json 文件
        totp_data_file = os.path.join(data_dir, "totp_data.json")
        if os.path.exists(totp_data_file):
            print(f"   totp_data.json 文件存在")
            with open(totp_data_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   文件内容长度: {len(content)} 字符")
                if content:
                    print(f"   文件内容: {content[:200]}...")
                else:
                    print("   文件为空")
        else:
            print("   totp_data.json 文件不存在")
    else:
        print("   数据目录不存在")
    
    print("\n=== 测试完成 ===")
    print(f"结论: 应用{'应该' if has_password else '不应该'}提示设置密码")

if __name__ == "__main__":
    test_password_detection()
