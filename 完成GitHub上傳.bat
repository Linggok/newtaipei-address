@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 完成 GitHub 上傳
echo ========================================
echo.
echo 請輸入您的 GitHub 專案網址
echo 例如：https://github.com/你的帳號/newtaipei-address.git
echo.
set /p GITHUB_URL="GitHub 專案網址："

if "%GITHUB_URL%"=="" (
    echo 錯誤：未輸入網址
    pause
    exit /b 1
)

echo.
echo [1/2] 連接 GitHub 專案...
git remote add origin %GITHUB_URL%
if errorlevel 1 (
    echo 警告：可能已經連接過，嘗試更新...
    git remote set-url origin %GITHUB_URL%
)

echo.
echo [2/2] 上傳到 GitHub...
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
    echo 3. 專案網址不正確
    echo.
    echo 如果要求 Personal Access Token：
    echo 1. 前往：https://github.com/settings/tokens
    echo 2. 點選「Generate new token (classic)」
    echo 3. 勾選 repo 權限
    echo 4. 產生並複製 token
    echo 5. 在密碼欄位貼上 token
    echo.
) else (
    echo.
    echo ========================================
    echo 完成！
    echo ========================================
    echo.
    echo 專案已上傳到 GitHub
    echo 下一步：前往 Render 部署
    echo.
)

pause
