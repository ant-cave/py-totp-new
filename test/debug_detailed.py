#!/usr/bin/env python3
"""
详细调试脚本 - 深入诊断加密解密问题
"""

import sys
import os
import base64
sys.path.append(os.path.dirname(__file__))

from src.core.encryption import EncryptionManager
from src.core.totp_manager import TOTPManager

def debug_encryption_detailed():
    """详细调试加密解密过程"""
    print("=== 详细调试加密解密过程 ===")
    
    # 创建加密管理器
    enc_manager = EncryptionManager()
    
    print("1. 初始化加密系统...")
    if not enc_manager.initialize_encryption("test_password"):
        print("❌ 加密管理器初始化失败")
        return False
    print("   ✓ 加密管理器初始化成功")
    
    print("2. 测试加密解密过程...")
    test_secret = "JBSWY3DPEHPK3PXP"  # 标准测试密钥
    print(f"   原始密钥: {test_secret}")
    
    # 加密密钥
    encrypted_result = enc_manager.encrypt_totp_key(test_secret)
    if not encrypted_result:
        print("❌ 加密TOTP密钥失败")
        return False
    
    encrypted_key, salt = encrypted_result
    print(f"   加密密钥: {base64.b64encode(encrypted_key).decode()}")
    print(f"   盐值: {base64.b64encode(salt).decode()}")
    
    # 解密密钥
    decrypted_key = enc_manager.decrypt_totp_key(encrypted_key, salt)
    if not decrypted_key:
        print("❌ 解密TOTP密钥失败")
        return False
    
    print(f"   解密密钥: {decrypted_key}")
    
    # 验证解密后的密钥是否与原始密钥相同
    if decrypted_key == test_secret:
        print("   ✓ 加密解密验证成功")
    else:
        print(f"   ❌ 加密解密验证失败: 期望 '{test_secret}', 得到 '{decrypted_key}'")
        return False
    
    print("3. 测试TOTP代码生成...")
    import pyotp
    try:
        totp = pyotp.TOTP(decrypted_key)
        code = totp.now()
        print(f"   ✓ TOTP代码生成成功: {code}")
    except Exception as e:
        print(f"   ❌ TOTP代码生成失败: {e}")
        return False
    
    return True

def debug_totp_manager_detailed():
    """详细调试TOTP管理器"""
    print("\n=== 详细调试TOTP管理器 ===")
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    print("1. 初始化加密系统...")
    if not totp_manager.initialize_with_password("test_password"):
        print("❌ 加密管理器初始化失败")
        return False
    print("   ✓ 加密管理器初始化成功")
    
    print("2. 添加TOTP条目...")
    test_secret = "JBSWY3DPEHPK3PXP"
    success = totp_manager.add_entry("Test Service", test_secret, "test@example.com")
    if success:
        print("   ✓ TOTP条目添加成功")
    else:
        print("   ❌ TOTP条目添加失败")
        return False
    
    print("3. 获取条目并生成TOTP代码...")
    entries = totp_manager.get_all_entries()
    if entries:
        entry = entries[0]
        print(f"   条目: {entry.name}")
        print(f"   加密密钥存在: {entry.encrypted_key is not None}")
        print(f"   盐值存在: {entry.salt is not None}")
        
        # 直接使用加密管理器解密
        print("4. 直接解密测试...")
        if entry.encrypted_key and entry.salt:
            decrypted_key = totp_manager.encryption.decrypt_totp_key(entry.encrypted_key, entry.salt)
            if decrypted_key:
                print(f"   ✓ 直接解密成功: {decrypted_key}")
                # 验证解密后的密钥
                if decrypted_key == test_secret:
                    print("   ✓ 密钥验证成功")
                else:
                    print(f"   ❌ 密钥验证失败: 期望 '{test_secret}', 得到 '{decrypted_key}'")
            else:
                print("   ❌ 直接解密失败")
        
        # 使用TOTP管理器生成代码
        print("5. 使用TOTP管理器生成代码...")
        code = totp_manager.generate_totp(entry)
        if code:
            print(f"   ✓ TOTP代码生成成功: {code}")
        else:
            print("   ❌ TOTP代码生成失败")
            return False
    else:
        print("   ❌ 没有找到条目")
        return False
    
    return True

if __name__ == "__main__":
    # 先测试基本的加密解密
    if debug_encryption_detailed():
        print("\n" + "="*50)
        # 再测试TOTP管理器
        debug_totp_manager_detailed()
    else:
        print("\n基本加密解密测试失败，无法继续测试TOTP管理器")
