"""
测试密码验证功能
验证密码正确和错误的情况
"""

import sys
import os
from pathlib import Path

# 添加src目录到路径
sys.path.append('src')

from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager

def test_password_verification():
    """测试密码验证功能"""
    print("=== 测试密码验证功能 ===")
    
    # 创建TOTP管理器并设置密码
    totp_manager = TOTPManager()
    test_password = "test123"
    
    print("1. 设置密码和测试条目...")
    if totp_manager.initialize_with_password(test_password):
        print("  密码设置成功")
        if totp_manager.add_entry("测试服务", "JBSWY3DPEHPK3PXP"):
            print("  测试条目添加成功")
        else:
            print("  测试条目添加失败")
            return
    else:
        print("  密码设置失败")
        return
    
    # 获取第一个条目的盐值用于验证
    entries = totp_manager.get_all_entries()
    if not entries:
        print("  没有找到条目")
        return
    
    first_entry = entries[0]
    salt = first_entry.salt
    
    print(f"\n2. 使用盐值测试密码验证:")
    print(f"  盐值: {salt.hex()[:16]}...")
    
    # 测试正确密码
    encryption = EncryptionManager()
    correct_result = encryption.validate_password(test_password, salt)
    print(f"  正确密码验证结果: {correct_result}")
    
    # 测试错误密码
    wrong_result = encryption.validate_password("wrongpassword", salt)
    print(f"  错误密码验证结果: {wrong_result}")
    
    # 测试主窗口的验证方法
    print(f"\n3. 测试主窗口验证方法:")
    
    # 模拟主窗口的验证逻辑
    def verify_and_unlock(password: str, totp_mgr: TOTPManager) -> bool:
        """模拟主窗口的验证方法"""
        try:
            # 首先加载数据来获取条目
            totp_mgr._load_data()
            
            # 获取第一个条目的盐值来测试密码
            entries = totp_mgr.get_all_entries()
            if not entries:
                return False
            
            # 使用第一个条目的盐值来验证密码
            first_entry = entries[0]
            if not first_entry.salt:
                return False
            
            # 使用加密管理器的验证方法
            return totp_mgr.encryption.validate_password(password, first_entry.salt)
        except Exception:
            return False
    
    # 创建新的TOTP管理器模拟重新启动
    totp_manager2 = TOTPManager()
    
    correct_main_result = verify_and_unlock(test_password, totp_manager2)
    print(f"  主窗口正确密码验证: {correct_main_result}")
    
    wrong_main_result = verify_and_unlock("wrongpassword", totp_manager2)
    print(f"  主窗口错误密码验证: {wrong_main_result}")
    
    print("\n=== 测试完成 ===")
    
    # 清理
    data_file = Path("data") / "totp_data.json"
    if data_file.exists():
        data_file.unlink()
        print("已清理测试数据文件")

if __name__ == "__main__":
    test_password_verification()
