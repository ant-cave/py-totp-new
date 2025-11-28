#!/usr/bin/env python3
"""
逐步调试加密解密过程
"""

import sys
import os
import base64
sys.path.append(os.path.dirname(__file__))

from src.core.encryption import EncryptionManager
from src.core.totp_manager import TOTPManager

def debug_encryption_step_by_step():
    """逐步调试加密解密过程"""
    print("=== 逐步调试加密解密过程 ===")
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    print("1. 初始化加密系统...")
    if not totp_manager.initialize_with_password("test_password"):
        print("❌ 加密管理器初始化失败")
        return False
    print("   ✓ 加密管理器初始化成功")
    
    print("2. 检查加密系统状态...")
    print(f"   加密系统已初始化: {totp_manager.is_encryption_initialized()}")
    print(f"   当前盐值: {totp_manager.encryption.get_salt()}")
    
    print("3. 添加TOTP条目...")
    test_secret = "JBSWY3DPEHPK3PXP"
    print(f"   原始密钥: {test_secret}")
    
    # 手动测试加密过程
    print("4. 手动测试加密过程...")
    encrypted_result = totp_manager.encryption.encrypt_totp_key(test_secret)
    if not encrypted_result:
        print("❌ 加密TOTP密钥失败")
        return False
    
    encrypted_key, salt = encrypted_result
    print(f"   加密密钥: {base64.b64encode(encrypted_key).decode()}")
    print(f"   盐值: {base64.b64encode(salt).decode()}")
    
    print("5. 手动测试解密过程...")
    decrypted_key = totp_manager.encryption.decrypt_totp_key(encrypted_key, salt, "test_password")
    if not decrypted_key:
        print("❌ 解密TOTP密钥失败")
        return False
    
    print(f"   解密密钥: {decrypted_key}")
    
    # 验证解密后的密钥
    if decrypted_key == test_secret:
        print("   ✓ 加密解密验证成功")
    else:
        print(f"   ❌ 加密解密验证失败: 期望 '{test_secret}', 得到 '{decrypted_key}'")
        return False
    
    print("6. 使用TOTP管理器添加条目...")
    success = totp_manager.add_entry("Test Service", test_secret, "test@example.com")
    if success:
        print("   ✓ TOTP条目添加成功")
    else:
        print("   ❌ TOTP条目添加失败")
        return False
    
    print("7. 获取条目并检查...")
    entries = totp_manager.get_all_entries()
    if entries:
        entry = entries[0]
        print(f"   条目名称: {entry.name}")
        print(f"   加密密钥存在: {entry.encrypted_key is not None}")
        print(f"   盐值存在: {entry.salt is not None}")
        
        if entry.encrypted_key and entry.salt:
            print(f"   条目加密密钥: {base64.b64encode(entry.encrypted_key).decode()}")
            print(f"   条目盐值: {base64.b64encode(entry.salt).decode()}")
            
            print("8. 使用TOTP管理器生成代码...")
            code = totp_manager.generate_totp(entry)
            if code:
                print(f"   ✓ TOTP代码生成成功: {code}")
            else:
                print("   ❌ TOTP代码生成失败")
                
                # 尝试手动解密
                print("9. 尝试手动解密条目密钥...")
                manual_decrypted = totp_manager.encryption.decrypt_totp_key(entry.encrypted_key, entry.salt, "test_password")
                if manual_decrypted:
                    print(f"   ✓ 手动解密成功: {manual_decrypted}")
                    if manual_decrypted == test_secret:
                        print("   ✓ 手动解密密钥验证成功")
                    else:
                        print(f"   ❌ 手动解密密钥验证失败: 期望 '{test_secret}', 得到 '{manual_decrypted}'")
                else:
                    print("   ❌ 手动解密失败")
                return False
        else:
            print("   ❌ 条目缺少加密密钥或盐值")
            return False
    else:
        print("   ❌ 没有找到条目")
        return False
    
    return True

if __name__ == "__main__":
    debug_encryption_step_by_step()
