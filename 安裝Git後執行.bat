@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 上傳專案到 GitHub
echo ========================================
echo.

REM 檢查 Git 是否已安裝
git --version >nul 2>&1
if errorlevel 1 (
    echo [錯誤] Git 尚未安裝
    echo.
    echo 請先安裝 Git：
    echo 1. 前往：https://git-scm.com/download/win
    echo 2. 下載並安裝 Git for Windows
    echo 3. 重新開啟此批次檔
    echo.
    echo 或使用 GitHub Desktop：
    echo https://desktop.github.com
    echo.
    pause
    exit /b 1
)

echo [檢查] Git 已安裝
git --version
echo.

echo [1/6] 初始化 Git...
if exist ".git" (
    echo Git 已初始化，跳過...
) else (
    git init
    if errorlevel 1 (
        echo 錯誤：無法初始化 Git
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
echo [5/6] 連接 GitHub 專案...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/Linggok/newtaipei-address.git
if errorlevel 1 (
    echo 警告：可能已經連接過
)

echo.
echo [6/6] 上傳到 GitHub...
echo.
echo 注意：可能會要求輸入 GitHub 帳號和密碼
echo 如果要求 Personal Access Token：
echo 1. 前往：https://github.com/settings/tokens
echo 2. Generate new token (classic)
echo 3. 勾選 repo 權限
echo 4. 產生並複製 token
echo 5. 在密碼欄位貼上 token
echo.
pause

git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo 上傳失敗
    echo ========================================
    echo.
    echo 可能的原因：
    echo 1. 需要登入 GitHub（會要求輸入帳號密碼）
    echo 2. 需要 Personal Access Token（不是密碼）
    echo 3. GitHub 專案尚未建立
    echo.
    echo 請確認：
    echo 1. 已在 GitHub 建立專案：https://github.com/Linggok/newtaipei-address
    echo 2. 已準備好 Personal Access Token（如果需要）
    echo.
) else (
    echo.
    echo ========================================
    echo 完成！
    echo ========================================
    echo.
    echo 專案已上傳到 GitHub
    echo 網址：https://github.com/Linggok/newtaipei-address
    echo.
    echo 下一步：前往 Render 部署
    echo https://render.com
    echo.
)

pause
