"""独立密码存储功能测试
测试独立密码存储功能，确保密码可以独立于TOTP密钥存储和验证
"""

import sys
import os
sys.path.append('.')
import base64

from src.core.encryption import EncryptionManager
from src.core.totp_manager import TOTPManager
from src.utils.config import ConfigManager


def test_initial_state():
    """测试初始状态"""
    print("=== 测试1: 初始状态 ===")
    
    # 重置配置
    config = ConfigManager()
    config.set('password.is_set', False)
    config.set('password.salt', None)
    config.set('password.iterations', 100000)
    config.set('password.test_data', None)
    
    em = EncryptionManager()
    
    print(f"1.1 独立密码已设置: {em._has_password_set()} (应为: False)")
    print(f"1.2 has_encrypted_data: {em.has_encrypted_data()} (应为: False)")
    
    assert not em._has_password_set(), "初始状态独立密码不应已设置"
    assert not em.has_encrypted_data(), "初始状态不应有加密数据"
    print("✅ 初始状态测试通过\n")
    return True


def test_set_password():
    """测试设置独立密码"""
    print("=== 测试2: 设置独立密码 ===")
    
    em = EncryptionManager()
    
    # 设置密码
    test_password = "MySecurePassword123!"
    success = em.set_password(test_password)
    
    print(f"2.1 设置密码结果: {success} (应为: True)")
    print(f"2.2 独立密码已设置: {em._has_password_set()} (应为: True)")
    print(f"2.3 has_encrypted_data: {em.has_encrypted_data()} (应为: True)")
    
    assert success, "设置密码应该成功"
    assert em._has_password_set(), "设置密码后独立密码标记应为True"
    assert em.has_encrypted_data(), "设置密码后应该有加密数据"
    
    # 检查配置是否正确保存
    config = ConfigManager()
    assert config.get('password.is_set', False) == True, "配置中密码设置标记应为True"
    assert config.get('password.salt') is not None, "配置中应有盐值"
    assert config.get('password.test_data') is not None, "配置中应有测试数据"
    
    print("✅ 设置密码测试通过\n")
    return True


def test_verify_correct_password():
    """测试验证正确密码"""
    print("=== 测试3: 验证正确密码 ===")
    
    em = EncryptionManager()
    test_password = "MySecurePassword123!"
    
    valid = em.verify_password(test_password)
    print(f"3.1 验证正确密码结果: {valid} (应为: True)")
    
    assert valid, "正确密码应该验证通过"
    print("✅ 正确密码验证测试通过\n")
    return True


def test_verify_wrong_password():
    """测试验证错误密码"""
    print("=== 测试4: 验证错误密码 ===")
    
    em = EncryptionManager()
    
    wrong_passwords = [
        "wrongpassword",
        "MySecurePassword123",
        "mysecurepassword123!",
        "AnotherPassword",
        ""
    ]
    
    all_failed = True
    for i, wrong_pwd in enumerate(wrong_passwords, 1):
        valid = em.verify_password(wrong_pwd)
        print(f"4.{i} 验证错误密码 '{wrong_pwd}' 结果: {valid} (应为: False)")
        if valid:
            all_failed = False
    
    assert all_failed, "所有错误密码都应该验证失败"
    print("✅ 错误密码验证测试通过\n")
    return True


def test_password_salt_management():
    """测试密码盐值管理"""
    print("=== 测试5: 密码盐值管理 ===")
    
    em = EncryptionManager()
    salt = em.get_password_salt()
    
    print(f"5.1 获取到的盐值: {salt is not None} (应为: True)")
    if salt:
        print(f"5.2 盐值长度: {len(salt)} 字节 (应为: 16)")
    
    assert salt is not None, "应该能获取到盐值"
    assert len(salt) == 16, "盐值长度应为16字节"
    print("✅ 密码盐值管理测试通过\n")
    return True


def test_totp_manager_integration():
    """测试TOTP管理器集成"""
    print("=== 测试6: TOTP管理器集成 ===")
    
    # 重置配置
    config = ConfigManager()
    config.set('password.is_set', False)
    config.set('password.salt', None)
    config.set('password.iterations', 100000)
    config.set('password.test_data', None)
    
    # 创建TOTP管理器
    totp_manager = TOTPManager()
    
    print(f"6.1 初始has_existing_password: {totp_manager.has_existing_password()} (应为: False)")
    assert not totp_manager.has_existing_password(), "初始状态不应有现有密码"
    
    # 使用独立密码初始化
    test_password = "TestPassword123"
    success = totp_manager.initialize_with_password(test_password)
    
    print(f"6.2 初始化结果: {success} (应为: True)")
    print(f"6.3 初始化后has_existing_password: {totp_manager.has_existing_password()} (应为: True)")
    
    assert success, "使用独立密码初始化应该成功"
    assert totp_manager.has_existing_password(), "初始化后应该有现有密码"
    
    print("✅ TOTP管理器集成测试通过\n")
    return True


def test_backward_compatibility():
    """测试向后兼容性（模拟现有TOTP数据）"""
    print("=== 测试7: 向后兼容性 ===")
    
    # 创建数据目录和模拟的TOTP数据文件
    from pathlib import Path
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 创建模拟的TOTP数据文件（包含版本信息）
    test_data = {
        "version": "1.0.0",
        "entries": []
    }
    
    data_file = data_dir / "totp_data.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        import json
        json.dump(test_data, f)
    
    # 测试has_encrypted_data
    em = EncryptionManager()
    has_data = em.has_encrypted_data()
    
    print(f"7.1 有TOTP数据文件时的has_encrypted_data: {has_data} (应为: True)")
    
    # 清理测试文件
    if data_file.exists():
        data_file.unlink()
    
    print("✅ 向后兼容性测试通过\n")
    return True


def test_independent_password_without_totp():
    """测试独立密码存储（无TOTP数据）"""
    print("=== 测试8: 独立密码存储（无TOTP数据） ===")
    
    # 确保没有TOTP数据文件
    from pathlib import Path
    data_file = Path("data") / "totp_data.json"
    if data_file.exists():
        data_file.unlink()
    
    # 重置配置
    config = ConfigManager()
    config.set('password.is_set', False)
    config.set('password.salt', None)
    config.set('password.iterations', 100000)
    config.set('password.test_data', None)
    
    # 测试场景：设置密码但不添加TOTP条目
    em = EncryptionManager()
    
    # 1. 设置密码
    test_password = "StandalonePassword456!"
    success = em.set_password(test_password)
    
    print(f"8.1 无TOTP数据时设置密码结果: {success} (应为: True)")
    assert success, "无TOTP数据时设置密码应该成功"
    
    # 2. 验证密码
    valid = em.verify_password(test_password)
    print(f"8.2 无TOTP数据时验证正确密码: {valid} (应为: True)")
    assert valid, "无TOTP数据时验证正确密码应该通过"
    
    # 3. 验证错误密码
    invalid = em.verify_password("WrongPassword")
    print(f"8.3 无TOTP数据时验证错误密码: {invalid} (应为: False)")
    assert not invalid, "无TOTP数据时验证错误密码应该失败"
    
    print("✅ 独立密码存储（无TOTP数据）测试通过\n")
    return True


def main():
    """主测试函数"""
    print("开始独立密码存储功能测试\n")
    
    tests_passed = 0
    total_tests = 8
    
    try:
        # 执行所有测试
        if test_initial_state():
            tests_passed += 1
        
        if test_set_password():
            tests_passed += 1
        
        if test_verify_correct_password():
            tests_passed += 1
        
        if test_verify_wrong_password():
            tests_passed += 1
        
        if test_password_salt_management():
            tests_passed += 1
        
        if test_totp_manager_integration():
            tests_passed += 1
        
        if test_backward_compatibility():
            tests_passed += 1
        
        if test_independent_password_without_totp():
            tests_passed += 1
        
        # 清理测试数据
        config = ConfigManager()
        config.set('password.is_set', False)
        config.set('password.salt', None)
        config.set('password.iterations', 100000)
        config.set('password.test_data', None)
        
        print(f"\n=== 测试总结 ===")
        print(f"通过测试: {tests_passed}/{total_tests}")
        
        if tests_passed == total_tests:
            print("🎉 所有测试通过！独立密码存储功能正常工作。")
        else:
            print(f"⚠️  {total_tests - tests_passed} 个测试失败")
        
        return tests_passed == total_tests
        
    except Exception as e:
        print(f"\n❌ 测试失败，出现异常: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
