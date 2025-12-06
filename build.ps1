# PyInstaller Build Script - TOTP Password Manager
# Using UPX compression optimization, single file mode, no console window

# Configuration parameters
$UPX_PATH = "C:\Program Files\upx-5.0.2-win64\upx.exe"
$ICON_PATH = "icon.ico"
$MAIN_FILE = "main.py"
$OUTPUT_NAME = "totp_app"
$PROJECT_PATH = $PWD

# Check if UPX exists
if (-not (Test-Path $UPX_PATH)) {
    Write-Host "Warning: UPX path does not exist: $UPX_PATH" -ForegroundColor Yellow
    Write-Host "Will proceed without UPX compression" -ForegroundColor Yellow
    $UPX_PATH = $null
}

# Check if icon file exists
if (-not (Test-Path $ICON_PATH)) {
    Write-Host "Warning: Icon file does not exist: $ICON_PATH" -ForegroundColor Yellow
    $ICON_PATH = ""
}

# Build PyInstaller command arguments
$PyInstallerArgs = @(
    "--onefile",                    # Single file mode
    "--noconsole",                  # No console window
    "--name=$OUTPUT_NAME",          # Output filename
    "--clean",                      # Clean temporary files
    "--distpath", "dist",           # Output directory
    "--workpath", "build",          # Working directory
    "--specpath", ".",              # Spec file directory
    "--add-data", "icon.ico;.",     # Include icon file
    "--add-data", "data;data"       # Include data directory
)

# Add UPX parameters (if exists)
if ($UPX_PATH -ne $null) {
    $PyInstallerArgs += @(
        "--upx-dir", (Split-Path $UPX_PATH -Parent)
    )
}

# Add icon parameter (if exists)
if ($ICON_PATH -ne "") {
    $PyInstallerArgs += "--icon=$ICON_PATH"
}

# Exclude unnecessary libraries
$PyInstallerArgs += @(
    "--exclude-module", "tkinter",
    "--exclude-module", "matplotlib",
    "--exclude-module", "scipy",
    "--exclude-module", "numpy",
    "--exclude-module", "pandas",
    "--exclude-module", "PIL",
    "--exclude-module", "PyQt5",
    "--exclude-module", "wx"
)

# Add hidden imports (PySide6 and cryptography related)
$PyInstallerArgs += @(
    "--hidden-import", "PySide6",
    "--hidden-import", "PySide6.QtCore",
    "--hidden-import", "PySide6.QtGui", 
    "--hidden-import", "PySide6.QtWidgets",
    "--hidden-import", "PySide6.QtUiTools",
    "--hidden-import", "PySide6.QtNetwork",
    "--hidden-import", "cryptography",
    "--hidden-import", "cryptography.hazmat",
    "--hidden-import", "cryptography.hazmat.backends",
    "--hidden-import", "cryptography.hazmat.primitives",
    "--hidden-import", "cryptography.hazmat.primitives.kdf.pbkdf2",
    "--hidden-import", "pyotp"
)

# Add main file
$PyInstallerArgs += $MAIN_FILE

Write-Host "Starting TOTP Password Manager build..." -ForegroundColor Green
Write-Host "Project path: $PROJECT_PATH" -ForegroundColor Cyan
if ($UPX_PATH -ne $null) {
    Write-Host "UPX path: $UPX_PATH" -ForegroundColor Cyan
} else {
    Write-Host "UPX: Not used" -ForegroundColor Yellow
}
Write-Host "Icon file: $ICON_PATH" -ForegroundColor Cyan
Write-Host "Output name: $OUTPUT_NAME" -ForegroundColor Cyan

# Clean previous build files
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build" -ErrorAction SilentlyContinue
    Write-Host "Cleaned build directory" -ForegroundColor Yellow
}

if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist" -ErrorAction SilentlyContinue
    Write-Host "Cleaned dist directory" -ForegroundColor Yellow
}

# Activate virtual environment if exists
$vEnvPath = Join-Path $PROJECT_PATH ".venv"
$pythonExe = "python"
if (Test-Path $vEnvPath) {
    $pythonExe = Join-Path $vEnvPath "Scripts\python.exe"
    Write-Host "Using virtual environment: $vEnvPath" -ForegroundColor Cyan
}

# Execute PyInstaller
try {
    Write-Host "Running PyInstaller..." -ForegroundColor Green
    & $pythonExe -m PyInstaller @PyInstallerArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Build completed successfully!" -ForegroundColor Green
        Write-Host "Output file: dist\$OUTPUT_NAME.exe" -ForegroundColor Green
        
        # Display file size
        $OutputFile = "dist\$OUTPUT_NAME.exe"
        if (Test-Path $OutputFile) {
            $FileSize = (Get-Item $OutputFile).Length / 1MB
            Write-Host "File size: $([math]::Round($FileSize, 2)) MB" -ForegroundColor Yellow
            
            # Verify executable can run
            Write-Host "Verifying executable..." -ForegroundColor Cyan
            $Process = Start-Process -FilePath $OutputFile -PassThru -WindowStyle Hidden
            Start-Sleep -Seconds 2
            if (-not $Process.HasExited) {
                $Process.Kill()
                Write-Host "Executable verification passed" -ForegroundColor Green
            } else {
                Write-Host "Executable may have issues" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "Build failed! Exit code: $LASTEXITCODE" -ForegroundColor Red
        exit $LASTEXITCODE
    }
}
catch {
    Write-Host "Error during build process: $_" -ForegroundColor Red
    exit 1
}