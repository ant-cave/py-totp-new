#!/usr/bin/env python3
"""
测试完整的密码流程
模拟设置密码、保存数据，然后验证密码检测功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def test_complete_password_flow():
    """测试完整的密码流程"""
    print("=== 测试完整的密码流程 ===")
    
    # 创建TOTP管理器实例
    totp_manager = TOTPManager()
    
    print("1. 初始状态检查...")
    has_password = totp_manager.has_existing_password()
    print(f"   已有密码: {has_password}")
    
    if not has_password:
        print("2. 模拟设置密码...")
        test_password = "test123"
        
        # 初始化密码
        success = totp_manager.initialize_with_password(test_password)
        print(f"   密码初始化结果: {success}")
        
        if success:
            # 添加一个测试条目
            print("3. 添加测试条目...")
            add_success = totp_manager.add_entry("Test Service", "JBSWY3DPEHPK3PXP")
            print(f"   测试条目添加结果: {add_success}")
            
            # 保存数据（add_entry 内部会自动保存）
            print("   数据已保存")
        else:
            print("   密码初始化失败")
    
    print("4. 再次检查密码状态...")
    has_password_after = totp_manager.has_existing_password()
    print(f"   已有密码: {has_password_after}")
    
    print("5. 验证密码...")
    if has_password_after:
        # 使用主窗口中的验证逻辑
        # 首先加载数据
        totp_manager._load_data()
        entries = totp_manager.get_all_entries()
        
        if entries:
            first_entry = entries[0]
            if first_entry.salt and first_entry.encrypted_key:
                # 测试正确密码
                correct_result = totp_manager.encryption.validate_password_with_encrypted_data(
                    "test123", first_entry.salt, first_entry.encrypted_key
                )
                print(f"   正确密码验证结果: {correct_result}")
                
                # 测试错误密码
                wrong_result = totp_manager.encryption.validate_password_with_encrypted_data(
                    "wrongpassword", first_entry.salt, first_entry.encrypted_key
                )
                print(f"   错误密码验证结果: {wrong_result}")
            else:
                print("   条目缺少盐值或加密密钥")
        else:
            print("   没有条目可用于验证")
    
    print("6. 检查数据文件...")
    data_dir = "data"
    if os.path.exists(data_dir):
        files = os.listdir(data_dir)
        print(f"   数据文件: {files}")
        
        # 检查 totp_data.json 文件内容
        totp_data_file = os.path.join(data_dir, "totp_data.json")
        if os.path.exists(totp_data_file):
            with open(totp_data_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(f"   totp_data.json 内容长度: {len(content)} 字符")
                if content:
                    print(f"   文件内容预览: {content[:200]}...")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_complete_password_flow()
