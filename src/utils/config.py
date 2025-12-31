
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
配置管理器模块
处理应用的配置存储和读取
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理器类"""
    
    def __init__(self, config_file: str = "config.json"):
        # 使用当前工作目录下的data文件夹，确保便携性
        self.config_dir = Path("data")
        self.config_file = self.config_dir / config_file
        
        # 确保配置目录存在
        self.config_dir.mkdir(exist_ok=True)
        
        # 加载配置
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            "app": {
                "version": "1.0.0",
                "theme": "dark",
                "auto_lock": True,
                "lock_timeout": 300  # 5分钟
            },
            "window": {
                "width": 800,
                "height": 600,
                "x": 100,
                "y": 100
            },
            "encryption": {
                "algorithm": "AES",
                "key_derivation_iterations": 100000
            },
            "password": {
                "is_set": False,      # 标记密码是否已设置
                "salt": None,         # 密码验证盐值（Base64编码）
                "iterations": 100000, # 密码验证迭代次数
                "test_data": None     # 密码验证测试数据（Base64编码）
            }
        }
    
    def save_config(self) -> bool:
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> bool:
        """设置配置值"""
        keys = key.split('.')
        config = self._config
        
        # 遍历到最后一个键的父级
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # 设置值
        config[keys[-1]] = value
        return self.save_config()
    
    def get_app_config(self) -> Dict[str, Any]:
        """获取应用配置"""
        return self.get("app", {})
    
    def get_window_config(self) -> Dict[str, Any]:
        """获取窗口配置"""
        return self.get("window", {})
    
    def get_encryption_config(self) -> Dict[str, Any]:
        """获取加密配置"""
        return self.get("encryption", {})
