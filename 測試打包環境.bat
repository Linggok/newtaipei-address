@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 測試打包環境
echo ========================================
echo.

echo [1] 檢查 Node.js 版本...
call node --version
if errorlevel 1 (
    echo 錯誤：找不到 Node.js，請先安裝 Node.js 18 或以上版本
    pause
    exit /b 1
)

echo.
echo [2] 檢查 npm 版本...
call npm --version
if errorlevel 1 (
    echo 錯誤：找不到 npm
    pause
    exit /b 1
)

echo.
echo [3] 檢查必要檔案...
if not exist "server.js" (
    echo 錯誤：找不到 server.js
    pause
    exit /b 1
) else (
    echo   server.js 存在
)

if not exist "package.json" (
    echo 錯誤：找不到 package.json
    pause
    exit /b 1
) else (
    echo   package.json 存在
)

echo.
echo [4] 檢查依賴安裝狀態...
if not exist "node_modules" (
    echo   警告：node_modules 不存在，需要執行 npm install
) else (
    echo   node_modules 存在
    if exist "node_modules\.bin\pkg.cmd" (
        echo   pkg.cmd 存在
    ) else if exist "node_modules\.bin\pkg" (
        echo   pkg 存在
    ) else (
        echo   警告：pkg 未安裝，需要執行 npm install
    )
)

echo.
echo [5] 檢查 CSV 檔案...
set CSV_COUNT=0
for %%f in (*.csv) do (
    set /a CSV_COUNT+=1
)
echo   找到 %CSV_COUNT% 個 CSV 檔案

echo.
echo [6] 檢查 public 資料夾...
if exist "public" (
    echo   public 資料夾存在
) else (
    echo   警告：public 資料夾不存在
)

echo.
echo ========================================
echo 測試完成
echo ========================================
echo.
echo 如果所有檢查都通過，可以執行「建立可攜式版本.bat」
echo.
pause
