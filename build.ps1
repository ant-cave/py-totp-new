# PyInstaller 构建脚本
# 使用 UPX 压缩优化，单文件模式，无控制台窗口

# 设置参数
$UPX_PATH = "F:\Program Files\upx-5.0.2-win64\upx.exe"
$ICON_PATH = "icon.ico"
$MAIN_FILE = "main.py"
$OUTPUT_NAME = "totp_app"

# 检查 UPX 是否存在
if (-not (Test-Path $UPX_PATH)) {
    Write-Host "错误: UPX 路径不存在: $UPX_PATH" -ForegroundColor Red
    exit 1
}

# 检查图标文件是否存在
if (-not (Test-Path $ICON_PATH)) {
    Write-Host "警告: 图标文件不存在: $ICON_PATH" -ForegroundColor Yellow
    $ICON_PATH = ""
}

# 构建 PyInstaller 命令
$PyInstallerArgs = @(
    "--onefile",                    # 单文件模式
    "--noconsole",                  # 无控制台窗口
    "--name=$OUTPUT_NAME",          # 输出文件名
    "--clean",                      # 清理临时文件
    "--upx-dir", (Split-Path $UPX_PATH -Parent),  # UPX 目录
    "--distpath", "dist",           # 输出目录
    "--workpath", "build",          # 工作目录
    "--specpath", "."               # spec 文件目录
)

# 添加图标参数（如果存在）
if ($ICON_PATH -ne "") {
    $PyInstallerArgs += "--icon=$ICON_PATH"
}

# 添加排除不必要的库
$PyInstallerArgs += @(
    "--exclude-module", "tkinter",
    "--exclude-module", "matplotlib",
    "--exclude-module", "scipy",
    "--exclude-module", "numpy",
    "--exclude-module", "pandas",
    "--exclude-module", "PIL",
    "--exclude-module", "PyQt5",
    "--exclude-module", "PySide2",
    "--exclude-module", "wx"
)

# 添加隐藏导入（如果需要）
$PyInstallerArgs += @(
    "--hidden-import", "cryptography.hazmat.backends",
    "--hidden-import", "cryptography.hazmat.primitives",
    "--hidden-import", "cryptography.hazmat.primitives.kdf.pbkdf2"
)

# 添加主文件
$PyInstallerArgs += $MAIN_FILE

Write-Host "start..." -ForegroundColor Green
Write-Host "UPX path: $UPX_PATH" -ForegroundColor Cyan
Write-Host "icon file: $ICON_PATH" -ForegroundColor Cyan
Write-Host "exe name: $OUTPUT_NAME" -ForegroundColor Cyan

# 执行 PyInstaller
try {
    pyinstaller @PyInstallerArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "completed!" -ForegroundColor Green
        Write-Host "file: dist\$OUTPUT_NAME.exe" -ForegroundColor Green
        
        # 显示文件大小
        $OutputFile = "dist\$OUTPUT_NAME.exe"
        if (Test-Path $OutputFile) {
            $FileSize = (Get-Item $OutputFile).Length / 1MB
            Write-Host "文件大小: $([math]::Round($FileSize, 2)) MB" -ForegroundColor Yellow
        }
    } else {
        Write-Host "failed! $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}
catch {
    Write-Host "error!$_" -ForegroundColor Red
    exit 1
}
