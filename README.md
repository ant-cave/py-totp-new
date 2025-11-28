# TOTP密码管理器

一个现代化的TOTP（基于时间的一次性密码）管理器应用，使用PySide6和pyotp库构建，具有密码加密功能和模块化设计。

> **创作说明**：本项目由 Cline + DeepSeek 协作开发完成

## 功能特点

- 🔐 **安全加密**：使用主密码对TOTP密钥进行AES加密存储
- 🎨 **现代化界面**：使用PySide6构建的简洁美观的用户界面
- ⚡ **实时更新**：自动更新TOTP代码，显示剩余时间
- 🔍 **快速搜索**：支持按名称和发行者搜索条目
- 📱 **响应式设计**：支持窗口大小调整和分割视图
- 🛡️ **密码强度检查**：设置主密码时提供强度指示
- 🔄 **自动格式化**：TOTP密钥输入时自动格式化

## 项目结构

```
py-totp-new/
├── main.py                 # 主程序入口
├── requirements.txt        # 依赖包列表
├── README.md              # 项目说明
└── src/                   # 源代码目录
    ├── core/              # 核心业务逻辑
    │   ├── encryption.py  # 加密管理器
    │   └── totp_manager.py # TOTP管理器
    ├── ui/                # 用户界面
    │   ├── main_window.py # 主窗口
    │   ├── password_dialog.py # 密码对话框
    │   └── add_entry_dialog.py # 添加条目对话框
    └── utils/             # 工具类
        └── config.py      # 配置管理器
```

## 安装和使用

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python main.py
```

### 3. 首次使用

1. 首次运行时会提示设置主密码
2. 设置强密码（至少8个字符）
3. 密码设置成功后进入主界面

### 4. 添加TOTP条目

1. 点击工具栏的"➕ 添加"按钮
2. 输入条目名称（必填）
3. 输入TOTP密钥（必填）
4. 可选输入发行者信息
5. 点击"确定"保存

### 5. 使用TOTP代码

- 左侧列表显示所有TOTP条目
- 实时显示6位TOTP代码
- 进度条显示当前周期剩余时间
- 点击条目可在右侧查看大号显示

## 技术架构

### 模块化设计

应用采用模块化架构，各模块职责明确：

- **TOTPApp**：应用主类，协调各模块
- **EncryptionManager**：处理密码加密解密
- **TOTPManager**：管理TOTP条目和代码生成
- **ConfigManager**：处理应用配置
- **MainWindow**：主界面和用户交互
- **PasswordDialog**：密码设置和验证
- **AddEntryDialog**：添加和编辑TOTP条目

### 安全特性

- 使用PBKDF2密钥派生算法
- AES加密存储TOTP密钥
- 每个条目使用独立的盐值
- 密码强度验证
- 安全的密钥输入和显示

### 用户界面

- 现代化扁平化设计
- 响应式布局
- 实时进度指示
- 直观的操作流程
- 深色主题支持

## 开发说明

### 依赖库

- **PySide6**：现代化GUI框架
- **pyotp**：TOTP代码生成
- **cryptography**：加密功能

### 代码规范

- 使用类型注解
- 遵循PEP 8编码规范
- 模块化设计，低耦合
- 完善的错误处理
- 详细的文档字符串

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。
