@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "node_modules" (
    echo 正在安裝依賴...
    call npm install
)

echo 正在啟動新北市地址查詢服務...
echo 啟動後請在瀏覽器開啟: http://localhost:3000
echo 關閉此視窗即可停止服務.
echo.
node server.js

pause
