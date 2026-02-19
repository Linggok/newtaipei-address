@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 上傳專案到 GitHub
echo ========================================
echo.

REM 嘗試找到 Git
set GIT_CMD=
if exist "C:\Program Files\Git\cmd\git.exe" (
    set "GIT_CMD=C:\Program Files\Git\cmd\git.exe"
) else if exist "C:\Program Files (x86)\Git\cmd\git.exe" (
    set "GIT_CMD=C:\Program Files (x86)\Git\cmd\git.exe"
) else (
    echo [錯誤] 找不到 Git
    echo.
    echo 請確認：
    echo 1. Git 已正確安裝
    echo 2. 已重新開啟命令提示字元
    echo 3. 或將 Git 加入系統 PATH
    echo.
    pause
    exit /b 1
)

echo [檢查] 找到 Git
"%GIT_CMD%" --version
echo.

echo [1/5] 加入檔案到 Git...
"%GIT_CMD%" add .
if errorlevel 1 (
    echo 錯誤：無法加入檔案
    pause
    exit /b 1
)

echo.
echo [2/5] 提交檔案...
"%GIT_CMD%" commit -m "Initial commit"
if errorlevel 1 (
    echo 警告：可能沒有變更需要提交，或已經提交過
)

echo.
echo [3/5] 設定主分支...
"%GIT_CMD%" branch -M main
if errorlevel 1 (
    echo 警告：可能已經設定過
)

echo.
echo [4/5] 連接 GitHub 專案...
"%GIT_CMD%" remote remove origin >nul 2>&1
"%GIT_CMD%" remote add origin https://github.com/Linggok/newtaipei-address.git
if errorlevel 1 (
    echo 警告：可能已經連接過，嘗試更新...
    "%GIT_CMD%" remote set-url origin https://github.com/Linggok/newtaipei-address.git
)

echo.
echo [5/5] 上傳到 GitHub...
echo.
echo 注意：可能會要求輸入 GitHub 帳號和密碼
echo 如果要求 Personal Access Token：
echo 1. 前往：https://github.com/settings/tokens
echo 2. Generate new token (classic)
echo 3. 勾選 repo 權限
echo 4. 產生並複製 token
echo 5. 在密碼欄位貼上 token（不是密碼）
echo.
pause

"%GIT_CMD%" push -u origin main

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
