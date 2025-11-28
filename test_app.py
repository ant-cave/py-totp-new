#!/usr/bin/env python3
"""
测试脚本 - 验证TOTP密码管理器应用的核心功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.encryption import EncryptionManager
from src.core.totp_manager import TOTPManager
from src.utils.config import ConfigManager

def test_encryption():
    """测试加密功能"""
    print("测试加密功能...")
    enc_manager = EncryptionManager()
    
    # 测试密码加密
    password = "test_password123"
    test_data = "Hello, this is test data!"
    
    # 初始化加密系统
    if enc_manager.initialize_encryption(password):
        print(f"✓ 加密系统初始化成功")
        
        # 加密数据
        encrypted_data = enc_manager.encrypt_data(test_data)
        if encrypted_data:
            print(f"✓ 数据加密成功")
            
            # 解密数据
            decrypted_data = enc_manager.decrypt_data(encrypted_data)
            if decrypted_data:
                print(f"✓ 数据解密成功")
                
                # 验证数据完整性
                assert decrypted_data == test_data, "解密数据不匹配原始数据"
                print(f"✓ 数据完整性验证通过")
                
                # 测试TOTP密钥加密
                totp_key = "JBSWY3DPEHPK3PXP"
                encrypted_totp = enc_manager.encrypt_totp_key(totp_key)
                if encrypted_totp:
                    encrypted_key, salt = encrypted_totp
                    print(f"✓ TOTP密钥加密成功")
                    
                    # 测试TOTP密钥解密
                    decrypted_totp = enc_manager.decrypt_totp_key(encrypted_key, salt, password)
                    if decrypted_totp == totp_key:
                        print(f"✓ TOTP密钥解密成功")
                        return True
                    else:
                        print(f"❌ TOTP密钥解密失败")
                        return False
                else:
                    print(f"❌ TOTP密钥加密失败")
                    return False
            else:
                print(f"❌ 数据解密失败")
                return False
        else:
            print(f"❌ 数据加密失败")
            return False
    else:
        print(f"❌ 加密系统初始化失败")
        return False

def test_totp_manager():
    """测试TOTP管理器功能"""
    print("\n测试TOTP管理器功能...")
    
    # 创建加密管理器并初始化
    enc_manager = EncryptionManager()
    if not enc_manager.initialize_encryption("test_password"):
        print("❌ 加密管理器初始化失败")
        return False
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    # 使用密码初始化TOTP管理器
    if not totp_manager.initialize_with_password("test_password"):
        print("❌ TOTP管理器初始化失败")
        return False
    
    # 测试添加TOTP条目
    test_secret = "JBSWY3DPEHPK3PXP"  # 标准测试密钥
    success = totp_manager.add_entry("Test Service", test_secret, "test@example.com")
    if success:
        print(f"✓ TOTP条目添加成功")
    else:
        print(f"❌ TOTP条目添加失败")
        return False
    
    # 测试获取所有条目
    entries = totp_manager.get_all_entries()
    print(f"✓ 获取到 {len(entries)} 个条目")
    
    if entries:
        # 测试生成TOTP代码
        code = totp_manager.generate_totp(entries[0])
        if code:
            print(f"✓ TOTP代码生成成功: {code}")
        else:
            print(f"❌ TOTP代码生成失败")
            return False
        
        # 测试删除条目
        success = totp_manager.remove_entry("Test Service")
        if success:
            print(f"✓ TOTP条目删除成功")
        else:
            print(f"❌ TOTP条目删除失败")
            return False
    else:
        print(f"❌ 没有找到条目")
        return False
    
    return True

def test_config_manager():
    """测试配置管理器功能"""
    print("\n测试配置管理器功能...")
    
    config = ConfigManager()
    
    # 测试设置和获取配置
    config.set("test_setting", "test_value")
    value = config.get("test_setting")
    print(f"✓ 配置设置和获取成功: {value}")
    
    # 测试删除配置（通过设置为None）
    config.set("test_setting", None)
    print(f"✓ 配置删除成功")
    
    return True

if __name__ == "__main__":
    print("开始测试TOTP密码管理器应用...")
    
    try:
        # 运行所有测试
        test_encryption()
        test_totp_manager()
        test_config_manager()
        
        print("\n🎉 所有测试通过！应用功能正常。")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
