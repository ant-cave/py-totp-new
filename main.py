#!/usr/bin/env python3
"""
TOTP密码管理器主程序
使用PyQt6创建现代化界面，支持密码加密存储
"""

import sys
import base64
from io import BytesIO
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QTimer

from src.ui.main_window import MainWindow
from src.core.totp_manager import TOTPManager
from src.core.encryption import EncryptionManager
from src.utils.config import ConfigManager

ICON_BASE64='AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAvMDH/LzAx/zAwL/8wLy3/MC8u/zAvLf8wLy7/MC8t/zAvLf8vLy3/Ly8t/y8vLf8vLiz/Ly8v/y8wMP8vMDD/LzAx/y8wMP8sNUj/JkB4/yNBgf8iQH//Ij99/yVGh/8mSo3/JkqM/yZKjP8nSo3/KEeA/y03Sv8vLy//LzAx/zAwL/8sNUj/G1C//xRX5f8TVeP/EVHe/xBP2P8SU97/GWb4/xtr//8ca///HWz//x1t/v8iYND/LThL/y8vL/8wLy3/JUB4/xRX5P8TU9z/EUnC/xZLv/8YTL3/G028/x9Vxv8hae//Hm3+/x9t/f8fbv7/IG///ypKgv8vLy3/MC8u/yNBgv8TVeH/D0Gt/xIbMP9KT1r/RElW/1BUX/9gY2r/SGeh/yFv/P8gcP3/IXD9/yFy//8qT4//Ly8t/zAwLv8iQH//ElPd/w04l/8WFxn/Y2Fc/1RST/8tLCr/YV5X/1Rqj/8jcvz/InT//yJz//8jdP//KlCP/y8vLf8wLy3/JEaG/xNU3v8MN5T/Fxga/2NhXv9TUk//HSMt/zk9Qf8+UnP/ImTU/x1UsP8kZdL/JXf//ytQj/8vLi3/MC8t/ydMj/8bZvb/DTqX/xYWGP9iYFz/X1xX/0ZKT/9HVGn/MUJe/xgkNv8SFRj/KjlR/zN46/8rUZD/Ly4t/zAvLf8oTY//H3D//xla0P8WIzr/UVpo/1dqif9Yaoj/WGmG/0BqsP8VKUn/HCUw/zFJcf85dtz/K1GR/y8uLf8vLy3/KE2P/yFx//8hcv//J0yK/zxjp/8mdfr/J3Ht/x5Gh/8lbeX/H1aw/xktS/81WJP/Lnr4/yxRj/8vLi3/Ly8t/ylPj/8idP//I3T//yhRl/9AYpz/Jnj//yRr4v8XMFb/JW3j/yd4/v8odPH/Knj5/yh6//8tUo//Ly4s/y8uLf8qUI//JHX//yV2//8kZdL/QVV2/z5jnv8ZN2b/HEWI/yh4+/8oef3/KXn9/yl5/f8pe///LVOP/y8uLf8vLi3/K0uB/yV2/v8mdv3/Jnf9/ypt2/8zY7D/Ilq1/yd18/8pev7/KXr9/yp7/P8re/z/K3z+/y5Ogf8vLiz/Ly8v/y45S/8oaNH/J3j+/yd5//8oev//KHv//yl8//8qfP//K3z//yt8//8rff//K339/y1s0P8vOkr/Ly8v/y8wMf8vLy//LjlL/y1MgP8sUY3/LFGN/y1Sjf8tUo3/LVKN/y5Sjf8uUo3/LlON/y5OgP8vOkr/Ly8v/y8wMP8vMDH/LzAx/y8vL/8vLy3/Ly8t/y8vLf8vLy3/Ly4t/y8vLf8vLiz/Ly4s/y8uLP8vLiz/Ly8v/y8wMP8vMDD/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=='


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
