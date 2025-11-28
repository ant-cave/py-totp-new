"""
调试添加条目功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def debug_add_entry():
    """调试添加条目功能"""
    print("=== 调试添加条目功能 ===")
    
    # 创建TOTP管理器实例
    totp_manager = TOTPManager()
    
    print("1. 检查加密系统状态:")
    print(f"   - 加密系统已初始化: {totp_manager.encryption.is_initialized()}")
    print(f"   - 存在加密数据: {totp_manager.encryption.has_encrypted_data()}")
    print(f"   - 当前密码: {totp_manager._current_password}")
    
    # 模拟解锁过程
    print("\n2. 模拟解锁过程:")
    
    # 首先加载数据
    totp_manager._load_data()
    entries = totp_manager.get_all_entries()
    print(f"   - 现有条目数量: {len(entries)}")
    
    if entries:
        first_entry = entries[0]
        print(f"   - 第一个条目: {first_entry.name}")
        print(f"   - 第一个条目的盐值: {first_entry.salt is not None}")
        print(f"   - 第一个条目的加密密钥: {first_entry.encrypted_key is not None}")
        
        # 假设密码是"123456"（根据之前的测试）
        test_password = "123456"
        
        # 验证密码
        is_valid = totp_manager.encryption.validate_password_with_encrypted_data(
            test_password, 
            first_entry.salt,
            first_entry.encrypted_key
        )
        print(f"   - 密码验证结果: {is_valid}")
        
        if is_valid:
            # 解锁加密系统
            unlock_success = totp_manager.encryption.unlock(test_password, first_entry.salt)
            print(f"   - 解锁加密系统: {unlock_success}")
            
            # 设置当前密码
            totp_manager._current_password = test_password
            
            print(f"   - 解锁后加密系统状态: {totp_manager.encryption.is_initialized()}")
            print(f"   - 解锁后当前密码: {totp_manager._current_password}")
            
            # 测试添加条目
            print("\n3. 测试添加条目:")
            test_name = "测试条目"
            test_secret = "JBSWY3DPEHPK3PXP"
            test_issuer = "测试发行者"
            
            add_success = totp_manager.add_entry(test_name, test_secret, test_issuer)
            print(f"   - 添加条目结果: {add_success}")
            
            if not add_success:
                print("   - 添加失败原因分析:")
                print(f"     - 加密系统已初始化: {totp_manager.encryption.is_initialized()}")
                print(f"     - Fernet对象存在: {totp_manager.encryption._fernet is not None}")
                print(f"     - 盐值存在: {totp_manager.encryption._salt is not None}")
                
                # 测试加密功能
                test_encrypt = totp_manager.encryption.encrypt_totp_key(test_secret)
                print(f"     - 加密测试结果: {test_encrypt is not None}")
                
                if test_encrypt:
                    print(f"     - 加密成功，盐值: {test_encrypt[1] is not None}")
                else:
                    print("     - 加密失败")
        else:
            print("   - 密码验证失败，无法继续测试")
    else:
        print("   - 没有现有条目，无法测试解锁")

if __name__ == "__main__":
    debug_add_entry()
