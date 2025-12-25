#!/usr/bin/env python3

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
TOTP密码管理器主程序
使用PyQt6创建现代化界面，支持密码加密存储
"""

import sys
import base64
from typing import NoReturn

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap

from src.ui.main_window import MainWindow
from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager
from src.utils.config import ConfigManager

from load_icon_data import ICON_BASE64

class TOTPApp:
    """TOTP应用主类"""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("TOTP密码管理器")
        self.app.setApplicationVersion("1.0.0")
        
        # 设置应用图标（使用Base64硬编码）
        try:
            # 从Base64数据创建图标
            icon_data = base64.b64decode(ICON_BASE64)
            pixmap = QPixmap()
            pixmap.loadFromData(icon_data)
            icon = QIcon(pixmap)
            self.app.setWindowIcon(icon)
        except Exception as e:
            print(f"设置应用图标失败: {e}")
        
        # 初始化配置管理器
        self.config = ConfigManager()
        
        # 初始化加密管理器
        self.encryption = EncryptionManager()
        
        # 初始化TOTP管理器
        self.totp_manager = TOTPManager()
        
        # 创建主窗口
        self.main_window = MainWindow(self.totp_manager)
        
    def run(self):
        """运行应用"""
        self.main_window.show()
        return self.app.exec()


def main():
    """主函数"""
    try:
        app = TOTPApp()
        sys.exit(app.run())
    except Exception as e:
        print(f"应用启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
