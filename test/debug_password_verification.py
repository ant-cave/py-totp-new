#!/usr/bin/env python3
"""
调试密码验证功能
"""

import sys
import os
import base64
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def debug_password_verification():
    """调试密码验证功能"""
    print("=== 密码验证调试 ===")
    
    # 创建管理器实例
    manager = TOTPManager()
    
    # 检查是否有现有密码
    has_password = manager.has_existing_password()
    print(f"检测到现有密码: {has_password}")
    
    if has_password:
        # 获取所有条目
        entries = manager.get_all_entries()
        print(f"找到 {len(entries)} 个条目")
        
        if entries:
            first_entry = entries[0]
            print(f"第一个条目: {first_entry.name}")
            print(f"盐值: {first_entry.salt}")
            print(f"加密密钥: {first_entry.encrypted_key[:50]}...")
            
            # 测试密码验证
            print("\n=== 测试密码验证 ===")
            
            # 测试正确密码
            test_password = "test123"  # 请使用您设置的密码
            print(f"测试密码: {test_password}")
            
            # 使用验证方法
            is_valid = manager.encryption.validate_password(test_password, first_entry.salt)
            print(f"密码验证结果: {is_valid}")
            
            if not is_valid:
                print("❌ 密码验证失败")
                print("可能的原因:")
                print("1. 密码不正确")
                print("2. 盐值格式问题")
                print("3. 加密算法不匹配")
                
                # 检查盐值格式
                print(f"\n盐值类型: {type(first_entry.salt)}")
                if isinstance(first_entry.salt, str):
                    print("盐值是字符串，需要转换为字节")
                    try:
                        salt_bytes = base64.b64decode(first_entry.salt)
                        print(f"解码后的盐值: {salt_bytes}")
                        is_valid = manager.encryption.validate_password(test_password, salt_bytes)
                        print(f"使用解码盐值的验证结果: {is_valid}")
                    except Exception as e:
                        print(f"盐值解码错误: {e}")
            else:
                print("✅ 密码验证成功")
    
    return has_password

if __name__ == "__main__":
    debug_password_verification()
