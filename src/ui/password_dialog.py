
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
密码对话框模块
处理主密码的设置和验证
"""

import base64

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QFont, QIcon, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from load_icon_data import ICON_BASE64


class PasswordDialog(QDialog):
    """密码对话框类"""
    
    def __init__(self, parent=None, initial_setup=False):
        super().__init__(parent)
        self.initial_setup = initial_setup
        self.password = None
        
        self.setup_ui()
        self.setWindowTitle("设置主密码" if initial_setup else "输入主密码")
        self.setModal(True)
        self.resize(400, 300)
        icon_data = base64.b64decode(ICON_BASE64)
        self.setWindowFlag(Qt.Window) 
        pixmap = QPixmap()
        pixmap.loadFromData(icon_data)
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)  # 关键：设置窗口图标

    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title_label = QLabel("TOTP密码管理器")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 说明文字
        if self.initial_setup:
            description = QLabel("首次使用，请设置一个主密码来保护您的TOTP密钥")
        else:
            description = QLabel("请输入您的主密码来解锁应用")
        
        description.setFont(QFont("Arial", 10))
        description.setStyleSheet("color: #7f8c8d;")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # 密码输入组
        password_group = QGroupBox("主密码")
        password_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #3498db;
            }
        """)
        password_layout = QFormLayout(password_group)
        
        if self.initial_setup:
            # 初始设置：需要确认密码
            self.password_edit = QLineEdit()
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_edit.setPlaceholderText("输入主密码")
            self.password_edit.textChanged.connect(self.validate_passwords)
            password_layout.addRow("密码:", self.password_edit)
            
            self.confirm_edit = QLineEdit()
            self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.confirm_edit.setPlaceholderText("确认主密码")
            self.confirm_edit.textChanged.connect(self.validate_passwords)
            password_layout.addRow("确认:", self.confirm_edit)
        else:
            # 解锁：只需要输入密码
            self.password_edit = QLineEdit()
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.password_edit.setPlaceholderText("输入您的主密码")
            self.password_edit.returnPressed.connect(self.accept)
            password_layout.addRow("密码:", self.password_edit)
        
        # 显示密码复选框
        self.show_password = QCheckBox("显示密码")
        self.show_password.toggled.connect(self.toggle_password_visibility)
        password_layout.addRow("", self.show_password)
        
        # 密码强度指示器（仅初始设置）
        if self.initial_setup:
            self.strength_label = QLabel("密码强度: -")
            self.strength_label.setStyleSheet("color: #95a5a6; font-size: 10px;")
            password_layout.addRow("", self.strength_label)
        
        layout.addWidget(password_group)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        if not self.initial_setup:
            cancel_button = QPushButton("取消")
            cancel_button.clicked.connect(self.reject)
            cancel_button.setStyleSheet("""
                QPushButton {
                    background: #95a5a6;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: #7f8c8d;
                }
            """)
            button_layout.addWidget(cancel_button)
        
        self.ok_button = QPushButton("确定" if self.initial_setup else "解锁")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setEnabled(not self.initial_setup)  # 初始设置时需要验证
        self.ok_button.setStyleSheet("""
            QPushButton {
                background: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2980b9;
            }
            QPushButton:disabled {
                background: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        
        # 设置输入框样式
        input_style = """
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        self.password_edit.setStyleSheet(input_style)
        if self.initial_setup:
            self.confirm_edit.setStyleSheet(input_style)
    
    def toggle_password_visibility(self, checked):
        """切换密码可见性"""
        if checked:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            if self.initial_setup:
                self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
            if self.initial_setup:
                self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
    
    def validate_passwords(self):
        """验证密码"""
        if not self.initial_setup:
            return
        
        password = self.password_edit.text()
        confirm = self.confirm_edit.text()
        
        # 检查密码强度
        strength = self.calculate_password_strength(password)
        self.update_strength_indicator(strength)
        
        # 检查密码匹配
        if password and confirm:
            if password == confirm:
                self.ok_button.setEnabled(len(password) >= 8)
                if len(password) < 8:
                    self.strength_label.setText("密码强度: 弱 (至少8个字符)")
                    self.strength_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
            else:
                self.ok_button.setEnabled(False)
                self.strength_label.setText("密码不匹配")
                self.strength_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
        else:
            self.ok_button.setEnabled(False)
    
    def calculate_password_strength(self, password):
        """计算密码强度"""
        if not password:
            return 0
        
        score = 0
        
        # 长度评分
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        
        # 字符类型评分
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        char_types = sum([has_lower, has_upper, has_digit, has_special])
        score += min(char_types - 1, 2)  # 最多加2分
        
        return min(score, 4)  # 最大4分
    
    def update_strength_indicator(self, strength):
        """更新密码强度指示器"""
        if strength == 0:
            text = "密码强度: -"
            color = "#95a5a6"
        elif strength == 1:
            text = "密码强度: 弱"
            color = "#e74c3c"
        elif strength == 2:
            text = "密码强度: 中等"
            color = "#f39c12"
        elif strength == 3:
            text = "密码强度: 强"
            color = "#3498db"
        else:  # strength == 4
            text = "密码强度: 非常强"
            color = "#2ecc71"
        
        self.strength_label.setText(text)
        self.strength_label.setStyleSheet(f"color: {color}; font-size: 10px;")
    
    def get_password(self):
        """获取输入的密码"""
        return self.password_edit.text()
    
    def closeEvent(self, arg__1: QCloseEvent):
        """处理窗口关闭事件"""
        # 在未输入密码时点击叉叉直接退出，不弹出警告
        if not self.password_edit.text():
            self.reject()
        else:
            # 如果已经输入了密码，使用默认行为
            super().closeEvent(arg__1)
    
    def accept(self):
        """接受对话框"""
        password = self.password_edit.text()
        
        if not password:
            QMessageBox.warning(self, "警告", "请输入密码")
            return
        
        if self.initial_setup:
            confirm = self.confirm_edit.text()
            if password != confirm:
                QMessageBox.warning(self, "警告", "密码不匹配")
                return
            
            if len(password) < 8:
                QMessageBox.warning(self, "警告", "密码至少需要8个字符")
                return
        
        self.password = password
        super().accept()
