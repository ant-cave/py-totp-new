
"""Copyright (C) 2025 ANTmmmmm <ANTmmmmm@outlook.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

"""
加密管理器模块
使用密码对TOTP密钥进行加密存储
"""

import base64
import hashlib
import json
import os
from typing import Optional, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.utils.config import ConfigManager


class EncryptionManager:
    """加密管理器类"""
    
    def __init__(self):
        self.config = ConfigManager()
        self._fernet: Optional[Fernet] = None
        self._salt: Optional[bytes] = None
    
    def _generate_salt(self) -> bytes:
        """生成随机盐值"""
        return os.urandom(16)
    
    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """从密码派生密钥"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.config.get("encryption.key_derivation_iterations", 100000),
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def initialize_encryption(self, password: str) -> Optional[bytes]:
        """使用密码初始化加密系统，返回盐值（成功时）或None（失败时）"""
        try:
            self._salt = self._generate_salt()
            key = self._derive_key(password, self._salt)
            self._fernet = Fernet(key)
            return self._salt
        except Exception:
            return None
    
    def unlock(self, password: str, salt: bytes) -> bool:
        """使用密码解锁加密系统"""
        try:
            self._salt = salt
            key = self._derive_key(password, salt)
            self._fernet = Fernet(key)
            return True
        except Exception:
            return False
    
    def encrypt_data(self, data: str) -> Optional[bytes]:
        """加密数据"""
        if not self._fernet:
            return None
        
        try:
            return self._fernet.encrypt(data.encode())
        except Exception:
            return None
    
    def decrypt_data(self, encrypted_data: bytes) -> Optional[str]:
        """解密数据"""
        if not self._fernet:
            return None
        
        try:
            decrypted = self._fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception:
            return None
    
    def encrypt_totp_key(self, totp_key: str) -> Optional[Tuple[bytes, bytes]]:
        """加密TOTP密钥"""
        if not self._fernet:
            return None
        
        try:
            encrypted_key = self.encrypt_data(totp_key)
            if encrypted_key and self._salt:
                return (encrypted_key, self._salt)
            return None
        except Exception:
            return None
    
    def decrypt_totp_key(self, encrypted_data: bytes, salt: bytes, password: str) -> Optional[str]:
        """解密TOTP密钥"""
        try:
            # 使用提供的salt和密码重新派生密钥进行解密
            key = self._derive_key(password, salt)
            temp_fernet = Fernet(key)
            decrypted = temp_fernet.decrypt(encrypted_data)
            return decrypted.decode()
        except Exception:
            return None
    
    def get_salt(self) -> Optional[bytes]:
        """获取当前盐值"""
        return self._salt
    
    def is_initialized(self) -> bool:
        """检查加密系统是否已初始化"""
        return self._fernet is not None and self._salt is not None
    
    def has_encrypted_data(self) -> bool:
        """检查是否存在已加密的数据（用于判断是否已经设置过密码）"""
        from pathlib import Path
        data_file = Path("data") / "totp_data.json"
        if data_file.exists():
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 如果文件存在且包含版本信息或initialized标志，说明已经初始化过
                    return "version" in data or "initialized" in data
            except (json.JSONDecodeError, IOError):
                return False
        return False
    
    def clear(self):
        """清除加密状态"""
        self._fernet = None
        self._salt = None
    
    def validate_password(self, password: str, salt: bytes) -> bool:
        """验证密码是否正确"""
        try:
            # 尝试使用提供的密码和盐值派生密钥
            key = self._derive_key(password, salt)
            
            # 创建一个测试的Fernet实例
            test_fernet = Fernet(key)
            
            # 创建一个已知的测试数据并加密
            test_data = "totp_validation_test_2024"
            encrypted_test_data = test_fernet.encrypt(test_data.encode())
            
            # 现在使用不同的Fernet实例（使用相同密钥）来解密
            # 这模拟了重新启动应用后的解密过程
            new_fernet = Fernet(key)
            decrypted = new_fernet.decrypt(encrypted_test_data).decode()
            
            # 如果解密后的数据与原始数据匹配，密码正确
            return decrypted == test_data
        except Exception:
            # 如果解密失败（例如密钥不正确），返回False
            return False
    
    def validate_password_with_encrypted_data(self, password: str, salt: bytes, encrypted_data: bytes) -> bool:
        """使用实际的加密数据验证密码"""
        try:
            # 尝试使用提供的密码和盐值派生密钥
            key = self._derive_key(password, salt)
            
            # 创建一个Fernet实例
            fernet = Fernet(key)
            
            # 尝试解密实际的加密数据
            decrypted = fernet.decrypt(encrypted_data).decode()
            
            # 如果解密成功，密码正确
            return True
        except Exception:
            # 如果解密失败（例如密钥不正确），返回False
            return False
