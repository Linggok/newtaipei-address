@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 上傳專案到 GitHub
echo ========================================
echo.
echo 目前位置：%CD%
echo.

REM 檢查是否已經初始化 Git
if exist ".git" (
    echo [1/6] Git 已初始化
) else (
    echo [1/6] 初始化 Git...
    git init
    if errorlevel 1 (
        echo 錯誤：無法初始化 Git
        echo 請確認已安裝 Git
        pause
        exit /b 1
    )
)

echo.
echo [2/6] 加入檔案到 Git...
git add .
if errorlevel 1 (
    echo 錯誤：無法加入檔案
    pause
    exit /b 1
)

echo.
echo [3/6] 提交檔案...
git commit -m "Initial commit"
if errorlevel 1 (
    echo 警告：可能沒有變更需要提交，或已經提交過
)

echo.
echo [4/6] 設定主分支...
git branch -M main
if errorlevel 1 (
    echo 警告：可能已經設定過
)

echo.
echo ========================================
echo 下一步：連接 GitHub
echo ========================================
echo.
echo 請在 GitHub 建立新專案後，執行以下指令：
echo.
echo git remote add origin https://github.com/你的帳號/newtaipei-address.git
echo git push -u origin main
echo.
echo 或手動執行：
echo   1. 前往 https://github.com/new 建立新專案
echo   2. 複製專案網址
echo   3. 執行上述指令（替換成您的網址）
echo.
pause
