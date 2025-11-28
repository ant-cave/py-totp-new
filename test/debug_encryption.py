#!/usr/bin/env python3
"""
调试脚本 - 详细检查加密和解密过程
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.encryption import EncryptionManager

def debug_encryption():
    """调试加密功能"""
    print("=== 调试加密功能 ===")
    enc_manager = EncryptionManager()
    
    # 测试密码加密
    password = "test_password123"
    test_data = "Hello, this is test data!"
    
    print(f"1. 初始化加密系统...")
    if enc_manager.initialize_encryption(password):
        print(f"   ✓ 加密系统初始化成功")
        print(f"   Salt: {enc_manager.get_salt()}")
    else:
        print(f"   ❌ 加密系统初始化失败")
        return False
    
    print(f"2. 加密测试数据...")
    encrypted_data = enc_manager.encrypt_data(test_data)
    if encrypted_data:
        print(f"   ✓ 数据加密成功")
        print(f"   加密数据长度: {len(encrypted_data)}")
    else:
        print(f"   ❌ 数据加密失败")
        return False
    
    print(f"3. 解密测试数据...")
    decrypted_data = enc_manager.decrypt_data(encrypted_data)
    if decrypted_data:
        print(f"   ✓ 数据解密成功")
        print(f"   原始数据: {test_data}")
        print(f"   解密数据: {decrypted_data}")
        if decrypted_data == test_data:
            print(f"   ✓ 数据完整性验证通过")
        else:
            print(f"   ❌ 数据完整性验证失败")
            return False
    else:
        print(f"   ❌ 数据解密失败")
        return False
    
    print(f"4. 测试TOTP密钥加密...")
    totp_key = "JBSWY3DPEHPK3PXP"
    encrypted_totp = enc_manager.encrypt_totp_key(totp_key)
    if encrypted_totp:
        encrypted_key, salt = encrypted_totp
        print(f"   ✓ TOTP密钥加密成功")
        print(f"   加密密钥长度: {len(encrypted_key)}")
        print(f"   Salt: {salt}")
    else:
        print(f"   ❌ TOTP密钥加密失败")
        return False
    
    print(f"5. 测试TOTP密钥解密...")
    decrypted_totp = enc_manager.decrypt_totp_key(encrypted_key, salt)
    if decrypted_totp:
        print(f"   ✓ TOTP密钥解密成功")
        print(f"   原始TOTP密钥: {totp_key}")
        print(f"   解密TOTP密钥: {decrypted_totp}")
        if decrypted_totp == totp_key:
            print(f"   ✓ TOTP密钥完整性验证通过")
        else:
            print(f"   ❌ TOTP密钥完整性验证失败")
            return False
    else:
        print(f"   ❌ TOTP密钥解密失败")
        return False
    
    return True

if __name__ == "__main__":
    debug_encryption()
