#!/usr/bin/env python3
"""
简单调试脚本 - 测试TOTP管理器基本功能
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.totp_manager import TOTPManager

def debug_simple():
    """简单调试TOTP管理器"""
    print("=== 简单调试TOTP管理器 ===")
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    print("1. 初始化加密系统...")
    if not totp_manager.initialize_with_password("test_password"):
        print("❌ 加密管理器初始化失败")
        return False
    print("   ✓ 加密管理器初始化成功")
    
    print("2. 检查是否已初始化...")
    if totp_manager.is_encryption_initialized():
        print("   ✓ 加密系统已初始化")
    else:
        print("   ❌ 加密系统未初始化")
        return False
    
    print("3. 添加TOTP条目...")
    test_secret = "JBSWY3DPEHPK3PXP"
    success = totp_manager.add_entry("Test Service", test_secret, "test@example.com")
    if success:
        print("   ✓ TOTP条目添加成功")
    else:
        print("   ❌ TOTP条目添加失败")
        return False
    
    print("4. 立即生成TOTP代码...")
    entries = totp_manager.get_all_entries()
    if entries:
        entry = entries[0]
        code = totp_manager.generate_totp(entry)
        if code:
            print(f"   ✓ TOTP代码生成成功: {code}")
        else:
            print("   ❌ TOTP代码生成失败")
            return False
    else:
        print("   ❌ 没有找到条目")
        return False
    
    print("5. 创建新的TOTP管理器实例测试...")
    totp_manager2 = TOTPManager()
    if not totp_manager2.initialize_with_password("test_password"):
        print("❌ 新实例加密管理器初始化失败")
        return False
    
    entries2 = totp_manager2.get_all_entries()
    if entries2:
        entry2 = entries2[0]
        code2 = totp_manager2.generate_totp(entry2)
        if code2:
            print(f"   ✓ 新实例TOTP代码生成成功: {code2}")
        else:
            print("   ❌ 新实例TOTP代码生成失败")
            return False
    else:
        print("   ❌ 新实例没有找到条目")
        return False
    
    return True

if __name__ == "__main__":
    debug_simple()
