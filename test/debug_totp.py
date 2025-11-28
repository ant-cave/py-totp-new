#!/usr/bin/env python3
"""
调试脚本 - 详细检查TOTP管理器功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.encryption import EncryptionManager
from src.core.totp_manager import TOTPManager

def debug_totp_manager():
    """调试TOTP管理器功能"""
    print("=== 调试TOTP管理器功能 ===")
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    # 初始化加密系统
    if not totp_manager.initialize_with_password("test_password"):
        print("❌ 加密管理器初始化失败")
        return False
    
    print(f"1. 添加TOTP条目...")
    test_secret = "JBSWY3DPEHPK3PXP"  # 标准测试密钥
    success = totp_manager.add_entry("Test Service", test_secret, "test@example.com")
    if success:
        print(f"   ✓ TOTP条目添加成功")
    else:
        print(f"   ❌ TOTP条目添加失败")
        return False
    
    print(f"2. 获取所有条目...")
    entries = totp_manager.get_all_entries()
    print(f"   ✓ 获取到 {len(entries)} 个条目")
    
    if entries:
        entry = entries[0]
        print(f"   条目信息:")
        print(f"     - 名称: {entry.name}")
        print(f"     - 发行者: {entry.issuer}")
        print(f"     - 加密密钥: {entry.encrypted_key is not None}")
        print(f"     - 盐值: {entry.salt is not None}")
        
        print(f"3. 生成TOTP代码...")
        code = totp_manager.generate_totp(entry)
        if code:
            print(f"   ✓ TOTP代码生成成功: {code}")
        else:
            print(f"   ❌ TOTP代码生成失败")
            # 尝试手动调试
            print(f"   手动调试解密过程...")
            if entry.encrypted_key and entry.salt:
                # 使用TOTP管理器内部的加密管理器
                decrypted_key = totp_manager.encryption.decrypt_totp_key(entry.encrypted_key, entry.salt)
                if decrypted_key:
                    print(f"   ✓ 解密TOTP密钥成功: {decrypted_key}")
                    # 尝试直接使用pyotp生成代码
                    import pyotp
                    try:
                        totp = pyotp.TOTP(decrypted_key)
                        manual_code = totp.now()
                        print(f"   ✓ 手动TOTP代码生成成功: {manual_code}")
                    except Exception as e:
                        print(f"   ❌ 手动TOTP代码生成失败: {e}")
                else:
                    print(f"   ❌ 解密TOTP密钥失败")
            return False
        
        print(f"4. 删除条目...")
        success = totp_manager.remove_entry("Test Service")
        if success:
            print(f"   ✓ TOTP条目删除成功")
        else:
            print(f"   ❌ TOTP条目删除失败")
            return False
    else:
        print(f"   ❌ 没有找到条目")
        return False
    
    return True

if __name__ == "__main__":
    debug_totp_manager()
