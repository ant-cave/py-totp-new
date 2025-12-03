"""
主窗口UI模块
使用PyQt6创建现代化TOTP管理器界面
"""

import sys
import time
from typing import Optional
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QTextEdit, 
                            QListWidget, QListWidgetItem, QProgressBar,
                            QMessageBox, QDialog, QDialogButtonBox,
                            QFormLayout, QGroupBox, QSplitter, QFrame,
                            QTabWidget, QToolBar, QStatusBar, QApplication)
from PySide6.QtCore import Qt, QTimer, Signal, QSize
from PySide6.QtGui import QFont, QIcon, QPalette, QColor, QAction

from src.core.totp_manager import TOTPManager, TOTPEntry
from src.core.encryption import EncryptionManager
from src.ui.password_dialog import PasswordDialog
from src.ui.add_entry_dialog import AddEntryDialog



class ClickableLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
    
    def empty(self):
        pass

    def mousePressEvent(self, event):
        # 触发点击事件
        #print("QLabel 被点击了！")
        # 可以在这里 emit 一个信号
        if self.text() != "••••••":
            self.clicked()

    def clicked(self):
        # 自定义的点击处理逻辑
        self.setStyleSheet("""
            QLabel {
                color: rgb(46, 204, 46);
                letter-spacing: 4px;
                padding: 20px;
                border-radius: 8px;
            }
        """)
        QApplication.clipboard().setText(self.text())
        QTimer.singleShot(300, lambda: self.setStyleSheet("""
    QLabel {
        color: #e74c3c;
        letter-spacing: 4px;
        padding: 20px;
        border-radius: 8px;
    }
"""))

class TOTPItemWidget(QWidget):
    """TOTP条目小部件"""
    
    delete_requested = Signal(str)  # 删除请求信号
    
    def __init__(self, entry: TOTPEntry, parent=None):
        super().__init__(parent)
        self.entry = entry
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # 图标标签
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4CAF50, stop:1 #45a049);
                border-radius: 16px;
                color: white;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        
        # 设置图标文本（使用名称首字母）
        icon_text = self.entry.name[0].upper() if self.entry.name else "?"
        self.icon_label.setText(icon_text)
        
        # 信息布局
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # 名称标签
        self.name_label = QLabel(self.entry.name)
        self.name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.name_label.setStyleSheet("color: #2c3e50;")
        
        # 发行者标签
        if self.entry.issuer:
            self.issuer_label = QLabel(self.entry.issuer)
            self.issuer_label.setFont(QFont("Arial", 8))
            self.issuer_label.setStyleSheet("color: #7f8c8d;")
            info_layout.addWidget(self.issuer_label)
        
        info_layout.addWidget(self.name_label)
        
        # TOTP代码标签
        self.code_label = QLabel("••••••")
        self.code_label.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.code_label.setStyleSheet("color: #e74c3c; letter-spacing: 2px;")
        info_layout.addWidget(self.code_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background: #ecf0f1;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 2px;
            }
        """)
        info_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.icon_label)
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # 删除按钮
        self.delete_button = QPushButton("🗑️")
        self.delete_button.setFixedSize(30, 30)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #c0392b;
            }
            QPushButton:pressed {
                background: #a93226;
            }
        """)
        self.delete_button.setToolTip("删除此条目")
        self.delete_button.clicked.connect(self.on_delete_clicked)
        layout.addWidget(self.delete_button)
        
        # 设置最小尺寸
        self.setMinimumHeight(80)
        
        # 设置样式
        self.setStyleSheet("""
            TOTPItemWidget {
                background: white;
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                margin: 2px;
            }
            TOTPItemWidget:hover {
                background: #f8f9fa;
                border-color: #3498db;
            }
        """)
    
    def on_delete_clicked(self):
        """删除按钮点击事件"""
        self.delete_requested.emit(self.entry.name)


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self, totp_manager: TOTPManager):
        super().__init__()
        self.totp_manager = totp_manager
        self.current_password: Optional[str] = None
        
        self.setup_ui()
        self.setup_timers()
        # 先隐藏窗口，等密码验证成功后再显示
        self.hide()
        self.check_initialization()
    
    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("TOTP密码管理器")
        self.setGeometry(100, 100, 900, 600)
        
        # 设置现代化样式
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
            }
            QWidget {
                font-family: "Segoe UI", Arial, sans-serif;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建工具栏
        self.create_toolbar()
        
        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # 左侧列表
        self.create_entry_list(splitter)
        
        # 右侧详情
        self.create_detail_view(splitter)
        
        # 设置分割器比例
        splitter.setSizes([300, 600])
        
        main_layout.addWidget(splitter)
        
        # 创建状态栏
        self.create_statusbar()
    
    def create_toolbar(self):
        """创建工具栏"""
        toolbar = QToolBar("主工具栏")
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(toolbar)
        
        # 添加条目动作
        add_action = QAction("➕ 添加", self)
        add_action.triggered.connect(self.show_add_entry_dialog)
        toolbar.addAction(add_action)
        
        toolbar.addSeparator()
        
        # 刷新动作
        refresh_action = QAction("🔄 刷新", self)
        refresh_action.triggered.connect(self.refresh_all_codes)
        toolbar.addAction(refresh_action)
        
        # 设置动作
        settings_action = QAction("⚙️ 设置", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
    
    def create_entry_list(self, parent):
        """创建条目列表"""
        list_widget = QWidget()
        list_layout = QVBoxLayout(list_widget)
        list_layout.setContentsMargins(10, 10, 10, 10)
        
        # 标题
        title_label = QLabel("TOTP条目")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        list_layout.addWidget(title_label)
        
        # 搜索框
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("搜索条目...")
        self.search_edit.textChanged.connect(self.filter_entries)
        self.search_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        list_layout.addWidget(self.search_edit)
        
        # 条目列表
        self.entry_list = QListWidget()
        self.entry_list.setStyleSheet("""
            QListWidget {
                background: white;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                outline: none;
            }
            QListWidget::item {
                border: none;
                padding: 0px;
            }
            QListWidget::item:selected {
                background: transparent;
            }
        """)
        self.entry_list.currentItemChanged.connect(self.on_entry_selected)
        list_layout.addWidget(self.entry_list)
        
        parent.addWidget(list_widget)
    
    def create_detail_view(self, parent):
        """创建详情视图"""
        detail_widget = QWidget()
        detail_layout = QVBoxLayout(detail_widget)
        detail_layout.setContentsMargins(20, 20, 20, 20)
        
        # 详情标题
        self.detail_title = QLabel("选择条目查看详情")
        self.detail_title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.detail_title.setStyleSheet("color: #2c3e50; margin-bottom: 20px;")
        detail_layout.addWidget(self.detail_title)
        
        # 代码显示区域
        code_group = QGroupBox("TOTP代码")
        code_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
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
        code_layout = QVBoxLayout(code_group)
        
        self.code_display = ClickableLabel("••••••")
        self.code_display.setFont(QFont("Courier New", 32, QFont.Weight.Bold))
        self.code_display.setStyleSheet("""
            QLabel {
                color: #e74c3c;
                letter-spacing: 4px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                qproperty-alignment: AlignCenter;
            }
        """)


        code_layout.addWidget(self.code_display)
        
        # 进度条
        self.detail_progress = QProgressBar()
        self.detail_progress.setFixedHeight(8)
        self.detail_progress.setTextVisible(False)
        self.detail_progress.setStyleSheet("""
            QProgressBar {
                border: none;
                background: #ecf0f1;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2ecc71, stop:1 #27ae60);
                border-radius: 4px;
            }
        """)
        code_layout.addWidget(self.detail_progress)
        
        # 剩余时间标签
        self.time_label = QLabel("剩余时间: 30秒")
        self.time_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        code_layout.addWidget(self.time_label)
        
        detail_layout.addWidget(code_group)
        detail_layout.addStretch()
        
        parent.addWidget(detail_widget)
    
    def create_statusbar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        status_bar.addWidget(self.status_label)
        
        # 条目计数标签
        self.count_label = QLabel("条目: 0")
        status_bar.addPermanentWidget(self.count_label)
    
    def setup_timers(self):
        """设置定时器"""
        # TOTP更新定时器（每秒更新）
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_all_codes)
        self.update_timer.start(1000)
    
    def check_initialization(self):
        """检查初始化状态"""
        # 检查是否已经设置过密码（通过检查是否存在加密数据）
        if self.totp_manager.has_existing_password():
            # 已经有密码，显示输入密码对话框
            self.show_password_dialog(initial_setup=False)
        else:
            # 首次使用，显示设置密码对话框
            self.show_password_dialog(initial_setup=True)
    
    def show_password_dialog(self, initial_setup=False):
        """显示密码对话框"""
        dialog = PasswordDialog(self, initial_setup)
        result = dialog.exec()
        
        # 如果对话框被拒绝（用户点击取消或关闭窗口），直接退出应用
        if result == QDialog.DialogCode.Rejected:
            QApplication.quit()
            exit()
            return 0
        
        # 如果对话框被接受，处理密码
        if result == QDialog.DialogCode.Accepted:
            password = dialog.get_password()
            if initial_setup:
                if self.totp_manager.initialize_with_password(password):
                    self.current_password = password
                    self.status_label.setText("加密系统已初始化")
                    self.load_entries()
                    # 密码设置成功，显示主窗口
                    self.show()
                else:
                    QMessageBox.critical(self, "错误", "加密系统初始化失败")
            else:
                # 验证密码并解锁
                if self.verify_and_unlock(password):
                    # 解锁成功后加载数据
                    self.totp_manager._load_data()
                    self.current_password = password
                    self.status_label.setText("已解锁")
                    self.load_entries()
                    # 密码验证成功，显示主窗口
                    self.show()
                else:
                    QMessageBox.warning(self, "密码错误", "密码不正确，请重试")
                    # 重新显示密码对话框
                    self.show_password_dialog(initial_setup=False)
    
    def load_entries(self):
        """加载条目"""
        self.entry_list.clear()
        entries = self.totp_manager.get_all_entries()
        
        for entry in entries:
            item_widget = TOTPItemWidget(entry)
            # 连接删除信号
            item_widget.delete_requested.connect(self.on_delete_entry_requested)
            list_item = QListWidgetItem(self.entry_list)
            list_item.setSizeHint(item_widget.sizeHint())
            self.entry_list.addItem(list_item)
            self.entry_list.setItemWidget(list_item, item_widget)
        
        self.count_label.setText(f"条目: {len(entries)}")
        self.update_all_codes()
    
    def update_all_codes(self):
        """更新所有TOTP代码"""
        remaining_time = self.totp_manager.get_remaining_time()
        progress = self.totp_manager.get_progress_percentage()
        
        # 更新列表中的条目
        for i in range(self.entry_list.count()):
            item = self.entry_list.item(i)
            widget = self.entry_list.itemWidget(item)
            if widget and isinstance(widget, TOTPItemWidget):
                code = self.totp_manager.generate_totp(widget.entry)
                if code:
                    widget.code_label.setText(code)
                    widget.progress_bar.setValue(int(progress))
        
        # 更新详情视图
        if hasattr(self, 'current_entry'):
            code = self.totp_manager.generate_totp(self.current_entry)
            if code:
                self.code_display.setText(code)
                self.detail_progress.setValue(int(progress))
                self.time_label.setText(f"剩余时间: {remaining_time}秒")
    
    def refresh_all_codes(self):
        """刷新所有代码"""
        self.update_all_codes()
        self.status_label.setText("代码已刷新")
    
    def on_entry_selected(self, current, previous):
        """条目选择事件"""
        if current:
            widget = self.entry_list.itemWidget(current)
            if widget and isinstance(widget, TOTPItemWidget):
                self.current_entry = widget.entry
                self.show_entry_details(widget.entry)
    
    def show_entry_details(self, entry: TOTPEntry):
        """显示条目详情"""
        self.detail_title.setText(entry.name)
        if entry.issuer:
            self.detail_title.setText(f"{entry.name} - {entry.issuer}")
        
        code = self.totp_manager.generate_totp(entry)
        if code:
            self.code_display.setText(code)
    
    def filter_entries(self, text):
        """过滤条目"""
        for i in range(self.entry_list.count()):
            item = self.entry_list.item(i)
            widget = self.entry_list.itemWidget(item)
            if widget and isinstance(widget, TOTPItemWidget):
                entry = widget.entry
                match = (text.lower() in entry.name.lower() or 
                        text.lower() in entry.issuer.lower())
                item.setHidden(not match)
    
    def show_add_entry_dialog(self):
        """显示添加条目对话框"""
        dialog = AddEntryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name, secret, issuer = dialog.get_entry_data()
            if name and secret:
                if self.totp_manager.add_entry(name, secret, issuer):
                    self.status_label.setText(f"已添加: {name}")
                    self.load_entries()
                else:
                    QMessageBox.warning(self, "警告", "添加条目失败")
    
    def verify_and_unlock(self, password: str) -> bool:
        """验证密码并解锁系统"""
        try:
            # 首先加载数据来获取条目
            self.totp_manager._load_data()
            
            # 获取第一个条目的盐值和加密密钥来测试密码
            entries = self.totp_manager.get_all_entries()
            if not entries:
                return False
            
            # 使用第一个条目的盐值和加密密钥来验证密码
            first_entry = entries[0]
            if not first_entry.salt or not first_entry.encrypted_key:
                return False
            
            # 使用加密管理器的验证方法（使用实际的加密数据）
            is_valid = self.totp_manager.encryption.validate_password_with_encrypted_data(
                password, 
                first_entry.salt,
                first_entry.encrypted_key
            )
            
            # 如果验证成功，设置TOTP管理器的当前密码并解锁加密系统
            if is_valid:
                self.totp_manager._current_password = password
                # 解锁加密系统，使其能够加密新条目
                self.totp_manager.encryption.unlock(password, first_entry.salt)
                
            return is_valid
            
        except Exception:
            return False
    
    def on_delete_entry_requested(self, entry_name: str):
        """处理删除条目请求"""
        # 显示确认对话框
        reply = QMessageBox.question(
            self,
            "确认删除",
            f"确定要删除条目 '{entry_name}' 吗？\n此操作无法撤销。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 执行删除操作
            if self.totp_manager.remove_entry(entry_name):
                self.status_label.setText(f"已删除: {entry_name}")
                self.load_entries()
                
                # 如果删除的是当前选中的条目，清空详情视图
                if hasattr(self, 'current_entry') and self.current_entry.name == entry_name:
                    self.detail_title.setText("选择条目查看详情")
                    self.code_display.setText("••••••")
                    self.detail_progress.setValue(0)
                    self.time_label.setText("剩余时间: 30秒")
            else:
                QMessageBox.warning(self, "删除失败", f"无法删除条目 '{entry_name}'")
    
    def show_settings(self):
        """显示设置对话框"""
        QMessageBox.information(self, "设置", "设置功能开发中...")
