"""
完整流程调试：模拟用户第一次设置密码和第二次进入的情况
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def debug_complete_flow():
    """调试完整流程"""
    print("=== 完整流程调试 ===")
    
    # 模拟第一次使用：设置密码
    print("\n1. 第一次使用 - 设置密码:")
    totp_manager1 = TOTPManager()
    password = "123456"
    
    print(f"   - 初始状态 - 加密系统已初始化: {totp_manager1.encryption.is_initialized()}")
    print(f"   - 初始状态 - 存在加密数据: {totp_manager1.encryption.has_encrypted_data()}")
    
    # 初始化加密系统
    init_success = totp_manager1.initialize_with_password(password)
    print(f"   - 初始化加密系统: {init_success}")
    print(f"   - 初始化后 - 加密系统已初始化: {totp_manager1.encryption.is_initialized()}")
    print(f"   - 初始化后 - 当前密码: {totp_manager1._current_password}")
    
    # 添加一个测试条目
    if init_success:
        add_success = totp_manager1.add_entry("测试条目1", "JBSWY3DPEHPK3PXP", "测试发行者1")
        print(f"   - 添加第一个条目: {add_success}")
        
        # 检查数据文件
        import json
        from pathlib import Path
        data_file = Path("data") / "totp_data.json"
        if data_file.exists():
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"   - 数据文件条目数量: {len(data.get('entries', []))}")
                if data.get('entries'):
                    first_entry = data['entries'][0]
                    print(f"   - 第一个条目名称: {first_entry.get('name')}")
                    print(f"   - 第一个条目盐值: {first_entry.get('salt') is not None}")
                    print(f"   - 第一个条目加密密钥: {first_entry.get('encrypted_key') is not None}")
    
    print("\n2. 第二次使用 - 验证密码并添加新条目:")
    totp_manager2 = TOTPManager()
    
    print(f"   - 新实例 - 加密系统已初始化: {totp_manager2.encryption.is_initialized()}")
    print(f"   - 新实例 - 存在加密数据: {totp_manager2.encryption.has_encrypted_data()}")
    print(f"   - 新实例 - 当前密码: {totp_manager2._current_password}")
    
    # 加载数据
    totp_manager2._load_data()
    entries = totp_manager2.get_all_entries()
    print(f"   - 加载后条目数量: {len(entries)}")
    
    if entries:
        first_entry = entries[0]
        print(f"   - 第一个条目: {first_entry.name}")
        print(f"   - 第一个条目的盐值: {first_entry.salt is not None}")
        print(f"   - 第一个条目的加密密钥: {first_entry.encrypted_key is not None}")
        
        # 验证密码
        is_valid = totp_manager2.encryption.validate_password_with_encrypted_data(
            password, 
            first_entry.salt,
            first_entry.encrypted_key
        )
        print(f"   - 密码验证结果: {is_valid}")
        
        if is_valid:
            # 解锁加密系统
            unlock_success = totp_manager2.encryption.unlock(password, first_entry.salt)
            print(f"   - 解锁加密系统: {unlock_success}")
            
            # 设置当前密码
            totp_manager2._current_password = password
            
            print(f"   - 解锁后加密系统状态: {totp_manager2.encryption.is_initialized()}")
            print(f"   - 解锁后当前密码: {totp_manager2._current_password}")
            
            # 测试添加新条目
            print("\n3. 测试添加新条目:")
            add_success2 = totp_manager2.add_entry("测试条目2", "JBSWY3DPEHPK3PXP", "测试发行者2")
            print(f"   - 添加第二个条目: {add_success2}")
            
            if not add_success2:
                print("   - 添加失败原因分析:")
                print(f"     - 加密系统已初始化: {totp_manager2.encryption.is_initialized()}")
                print(f"     - Fernet对象存在: {totp_manager2.encryption._fernet is not None}")
                print(f"     - 盐值存在: {totp_manager2.encryption._salt is not None}")
                
                # 测试加密功能
                test_encrypt = totp_manager2.encryption.encrypt_totp_key("JBSWY3DPEHPK3PXP")
                print(f"     - 加密测试结果: {test_encrypt is not None}")
                
                if test_encrypt:
                    print(f"     - 加密成功，盐值: {test_encrypt[1] is not None}")
                else:
                    print("     - 加密失败")
        else:
            print("   - 密码验证失败")
    else:
        print("   - 没有现有条目")

if __name__ == "__main__":
    debug_complete_flow()
