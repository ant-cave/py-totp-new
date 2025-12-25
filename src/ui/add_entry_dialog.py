
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
添加条目对话框模块
处理TOTP条目的添加和编辑
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class AddEntryDialog(QDialog):
    """添加条目对话框类"""
    
    def __init__(self, parent=None, entry=None):
        super().__init__(parent)
        self.entry = entry  # 如果提供，则是编辑模式
        self.entry_data = None
        
        self.setup_ui()
        self.setWindowTitle("编辑TOTP条目" if entry else "添加TOTP条目")
        self.setModal(True)
        self.resize(500, 400)
        
        # 如果是编辑模式，填充现有数据
        if entry:
            self.fill_existing_data()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # 标题
        title_label = QLabel("添加TOTP条目" if not self.entry else "编辑TOTP条目")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # 基本信息组
        basic_group = QGroupBox("基本信息")
        basic_group.setStyleSheet("""
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
        basic_layout = QFormLayout(basic_group)
        
        # 名称输入
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如：Gmail、GitHub")
        self.name_edit.textChanged.connect(self.validate_inputs)
        basic_layout.addRow("名称*:", self.name_edit)
        
        # 发行者输入
        self.issuer_edit = QLineEdit()
        self.issuer_edit.setPlaceholderText("例如：Google、Microsoft")
        basic_layout.addRow("发行者:", self.issuer_edit)
        
        layout.addWidget(basic_group)
        
        # 密钥信息组
        key_group = QGroupBox("TOTP密钥")
        key_group.setStyleSheet(basic_group.styleSheet())
        key_layout = QFormLayout(key_group)
        
        # 密钥输入
        self.key_edit = QLineEdit()
        self.key_edit.setPlaceholderText("输入TOTP密钥（通常为32位字符）")
        self.key_edit.textChanged.connect(self.validate_inputs)
        key_layout.addRow("密钥*:", self.key_edit)
        
        # 密钥格式选项
        format_layout = QHBoxLayout()
        
        self.show_key = QCheckBox("显示密钥")
        self.show_key.toggled.connect(self.toggle_key_visibility)
        format_layout.addWidget(self.show_key)
        
        self.auto_format = QCheckBox("自动格式化")
        self.auto_format.setChecked(True)
        self.auto_format.toggled.connect(self.toggle_auto_format)
        format_layout.addWidget(self.auto_format)
        
        key_layout.addRow("选项:", format_layout)
        
        # 密钥验证状态
        self.key_status_label = QLabel("")
        self.key_status_label.setStyleSheet("color: #95a5a6; font-size: 10px;")
        key_layout.addRow("状态:", self.key_status_label)
        
        layout.addWidget(key_group)
        
        # 说明文字
        help_text = QLabel(
            "提示：TOTP密钥通常是32位字符的字符串，可以从支持2FA的应用中获取。\n"
            "密钥会自动去除空格和连字符进行验证。"
        )
        help_text.setFont(QFont("Arial", 9))
        help_text.setStyleSheet("color: #7f8c8d; background: #f8f9fa; padding: 10px; border-radius: 4px;")
        help_text.setWordWrap(True)
        layout.addWidget(help_text)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
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
        
        self.ok_button = QPushButton("确定" if not self.entry else "保存")
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setEnabled(False)
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
        self.name_edit.setStyleSheet(input_style)
        self.issuer_edit.setStyleSheet(input_style)
        self.key_edit.setStyleSheet(input_style)
    
    def fill_existing_data(self):
        """填充现有数据（编辑模式）"""
        if self.entry:
            self.name_edit.setText(self.entry.name)
            self.issuer_edit.setText(self.entry.issuer)
            # 注意：在编辑模式下，我们不显示密钥，因为它是加密的
            self.key_edit.setPlaceholderText("密钥已加密保存")
            self.key_edit.setEnabled(False)
            self.ok_button.setEnabled(True)
    
    def toggle_key_visibility(self, checked):
        """切换密钥可见性"""
        if checked:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.key_edit.setEchoMode(QLineEdit.EchoMode.Password)
    
    def toggle_auto_format(self, checked):
        """切换自动格式化"""
        if checked and self.key_edit.text():
            # 重新格式化当前文本
            self.format_key()
    
    def format_key(self):
        """格式化密钥（每4个字符添加空格）"""
        if not self.auto_format.isChecked():
            return
        
        text = self.key_edit.text()
        # 移除所有空格
        clean_text = text.replace(" ", "").replace("-", "")
        
        # 每4个字符添加空格
        formatted = ""
        for i in range(0, len(clean_text), 4):
            if formatted:
                formatted += " "
            formatted += clean_text[i:i+4]
        
        if formatted != text:
            # 阻止递归调用
            self.key_edit.blockSignals(True)
            self.key_edit.setText(formatted)
            self.key_edit.blockSignals(False)
    
    def validate_inputs(self):
        """验证输入"""
        name = self.name_edit.text().strip()
        key = self.key_edit.text()
        
        # 基本验证
        has_name = bool(name)
        has_key = bool(key)
        
        # 密钥格式验证
        key_valid = False
        if has_key:
            # 清理密钥进行验证
            clean_key = key.replace(" ", "").replace("-", "")
            key_valid = len(clean_key) >= 16  # 基本长度检查
            
            # 更新状态标签
            if len(clean_key) < 16:
                self.key_status_label.setText("密钥太短（至少16位）")
                self.key_status_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
            elif len(clean_key) > 64:
                self.key_status_label.setText("密钥太长（最多64位）")
                self.key_status_label.setStyleSheet("color: #e74c3c; font-size: 10px;")
            else:
                self.key_status_label.setText("格式正确")
                self.key_status_label.setStyleSheet("color: #2ecc71; font-size: 10px;")
        else:
            self.key_status_label.setText("")
        
        # 启用/禁用确定按钮
        self.ok_button.setEnabled(has_name and has_key and key_valid)
        
        # 自动格式化
        if self.auto_format.isChecked():
            self.format_key()
    
    def get_entry_data(self):
        """获取条目数据"""
        return (
            self.name_edit.text().strip(),
            self.key_edit.text().replace(" ", "").replace("-", ""),
            self.issuer_edit.text().strip()
        )
    
    def accept(self):
        """接受对话框"""
        name, key, issuer = self.get_entry_data()
        
        if not name:
            QMessageBox.warning(self, "警告", "请输入条目名称")
            return
        
        if not key:
            QMessageBox.warning(self, "警告", "请输入TOTP密钥")
            return
        
        # 基本密钥长度验证
        if len(key) < 16:
            QMessageBox.warning(self, "警告", "TOTP密钥至少需要16个字符")
            return
        
        if len(key) > 64:
            QMessageBox.warning(self, "警告", "TOTP密钥最多64个字符")
            return
        
        # 验证密钥格式（尝试创建TOTP对象）
        try:
            import pyotp
            totp = pyotp.TOTP(key)
            test_code = totp.now()
            if not (len(test_code) == 6 and test_code.isdigit()):
                raise ValueError("生成的代码格式不正确")
        except Exception as e:
            QMessageBox.warning(
                self, 
                "警告", 
                f"TOTP密钥格式不正确:\n{str(e)}\n\n请检查密钥是否正确。"
            )
            return
        
        self.entry_data = (name, key, issuer)
        super().accept()
