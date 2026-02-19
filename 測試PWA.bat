@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo PWA 測試工具
echo ========================================
echo.

echo [1] 檢查必要檔案...
if not exist "public\manifest.json" (
    echo   錯誤：找不到 manifest.json
    pause
    exit /b 1
) else (
    echo   manifest.json 存在
)

if not exist "public\service-worker.js" (
    echo   警告：找不到 service-worker.js
) else (
    echo   service-worker.js 存在
)

if not exist "public\icon-192.png" (
    echo   警告：找不到 icon-192.png（PWA 仍可運作，但可能沒有圖示）
) else (
    echo   icon-192.png 存在
)

if not exist "public\icon-512.png" (
    echo   警告：找不到 icon-512.png（PWA 仍可運作，但可能沒有圖示）
) else (
    echo   icon-512.png 存在
)

echo.
echo [2] 檢查 server.js...
if not exist "server.js" (
    echo   錯誤：找不到 server.js
    pause
    exit /b 1
) else (
    echo   server.js 存在
)

echo.
echo ========================================
echo 測試步驟
echo ========================================
echo.
echo 1. 啟動服務：npm start
echo 2. 在電腦瀏覽器開啟：http://localhost:3000
echo 3. 開啟開發者工具（F12）→ Application → Manifest
echo 4. 檢查是否有錯誤
echo.
echo 手機測試：
echo 1. 確認電腦和手機在同一網路
echo 2. 查詢電腦的 IP 位址：ipconfig
echo 3. 在手機瀏覽器開啟：http://你的IP:3000
echo 4. 嘗試安裝到主畫面
echo.
echo 或使用 ngrok 建立公開網址：
echo   npm install -g ngrok
echo   ngrok http 3000
echo.
pause
