"""
TOTP管理器模块
处理TOTP令牌的生成和管理
"""

import base64
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pyotp
from cryptography.fernet import Fernet

from src.core.encryption import EncryptionManager
from src.utils.config import ConfigManager


class TOTPEntry:
    """TOTP条目类"""
    
    def __init__(self, name: str, issuer: str = "", encrypted_key: bytes = None, 
                 salt: bytes = None, icon: str = ""):
        self.name = name
        self.issuer = issuer
        self.encrypted_key = encrypted_key
        self.salt = salt
        self.icon = icon
        self.created_time = time.time()
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "issuer": self.issuer,
            "encrypted_key": base64.b64encode(self.encrypted_key).decode() if self.encrypted_key else None,
            "salt": base64.b64encode(self.salt).decode() if self.salt else None,
            "icon": self.icon,
            "created_time": self.created_time
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TOTPEntry':
        """从字典创建实例"""
        entry = cls(
            name=data["name"],
            issuer=data.get("issuer", ""),
            icon=data.get("icon", "")
        )
        
        if data.get("encrypted_key") and data.get("salt"):
            entry.encrypted_key = base64.b64decode(data["encrypted_key"])
            entry.salt = base64.b64decode(data["salt"])
        
        entry.created_time = data.get("created_time", time.time())
        return entry


class TOTPManager:
    """TOTP管理器类"""
    
    def __init__(self):
        self.encryption = EncryptionManager()
        self.config = ConfigManager()
        # 使用data目录保存TOTP数据
        self.data_file = Path("data") / "totp_data.json"
        self._entries: List[TOTPEntry] = []
        self._current_password: Optional[str] = None
        
        # 确保data目录存在
        Path("data").mkdir(exist_ok=True)
        
        # 不自动加载数据，等待密码初始化后再加载
    
    def initialize_with_password(self, password: str) -> bool:
        """使用密码初始化加密系统"""
        success = self.encryption.initialize_encryption(password)
        if success:
            self._current_password = password
            self._load_data()
        return success
    
    def unlock_with_password(self, password: str, salt: bytes) -> bool:
        """使用密码解锁加密系统"""
        return self.encryption.unlock(password, salt)
    
    def is_encryption_initialized(self) -> bool:
        """检查加密系统是否已初始化"""
        return self.encryption.is_initialized()
    
    def has_existing_password(self) -> bool:
        """检查是否已经设置过密码（通过检查是否存在加密数据）"""
        return self.encryption.has_encrypted_data()
    
    def _load_data(self):
        """加载TOTP数据"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._entries = [TOTPEntry.from_dict(entry_data) for entry_data in data.get("entries", [])]
            except (json.JSONDecodeError, IOError):
                self._entries = []
        else:
            self._entries = []
    
    def _save_data(self) -> bool:
        """保存TOTP数据"""
        try:
            data = {
                "entries": [entry.to_dict() for entry in self._entries],
                "version": "1.0.0",
                "last_updated": time.time()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def add_entry(self, name: str, secret_key: str, issuer: str = "", icon: str = "") -> bool:
        """添加TOTP条目"""
        if not self.encryption.is_initialized():
            return False
        
        # 加密密钥
        encrypted_result = self.encryption.encrypt_totp_key(secret_key)
        if not encrypted_result:
            return False
        
        encrypted_key, salt = encrypted_result
        
        # 创建条目
        entry = TOTPEntry(
            name=name,
            issuer=issuer,
            encrypted_key=encrypted_key,
            salt=salt,
            icon=icon
        )
        
        self._entries.append(entry)
        return self._save_data()
    
    def remove_entry(self, name: str) -> bool:
        """移除TOTP条目"""
        self._entries = [entry for entry in self._entries if entry.name != name]
        return self._save_data()
    
    def get_entry(self, name: str) -> Optional[TOTPEntry]:
        """获取TOTP条目"""
        for entry in self._entries:
            if entry.name == name:
                return entry
        return None
    
    def get_all_entries(self) -> List[TOTPEntry]:
        """获取所有TOTP条目"""
        return self._entries.copy()
    
    def generate_totp(self, entry: TOTPEntry) -> Optional[str]:
        """生成TOTP代码"""
        if not entry.encrypted_key or not entry.salt or not self._current_password:
            return None
        
        # 解密密钥
        secret_key = self.encryption.decrypt_totp_key(entry.encrypted_key, entry.salt, self._current_password)
        if not secret_key:
            return None
        
        try:
            # 创建TOTP对象
            totp = pyotp.TOTP(secret_key)
            return totp.now()
        except Exception:
            return None
    
    def get_remaining_time(self) -> int:
        """获取当前TOTP周期的剩余时间（秒）"""
        return 30 - (int(time.time()) % 30)
    
    def get_progress_percentage(self) -> float:
        """获取当前周期的进度百分比"""
        remaining = self.get_remaining_time()
        return (30 - remaining) / 30 * 100
    
    def validate_secret_key(self, secret_key: str) -> bool:
        """验证TOTP密钥格式"""
        try:
            # 清理密钥（移除空格等）
            cleaned_key = secret_key.replace(" ", "").replace("-", "")
            
            # 尝试创建TOTP对象
            totp = pyotp.TOTP(cleaned_key)
            
            # 测试生成代码
            code = totp.now()
            return len(code) == 6 and code.isdigit()
        except Exception:
            return False
    
    def get_entry_count(self) -> int:
        """获取条目数量"""
        return len(self._entries)
    
    def clear_all_entries(self) -> bool:
        """清除所有条目"""
        self._entries.clear()
        return self._save_data()
    
    def update_entry(self, old_name: str, new_name: str, new_issuer: str = "", new_icon: str = "") -> bool:
        """更新TOTP条目信息"""
        for entry in self._entries:
            if entry.name == old_name:
                entry.name = new_name
                entry.issuer = new_issuer
                entry.icon = new_icon
                return self._save_data()
        return False
