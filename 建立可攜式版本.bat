@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo 新北市地址查詢系統 - 可攜式版本建立工具
echo ========================================
echo.

REM 檢查並安裝本地依賴
echo [1/5] 檢查並安裝本地依賴...
if not exist "node_modules" (
    echo 正在安裝專案依賴（包含 pkg）...
    call npm install
    if errorlevel 1 (
        echo 錯誤：無法安裝依賴，請檢查網路連線或手動執行: npm install
        pause
        exit /b 1
    )
) else (
    echo 檢查 pkg 是否已安裝...
    call npm list pkg >nul 2>&1
    if errorlevel 1 (
        echo 正在安裝 pkg...
        call npm install pkg --save-dev
        if errorlevel 1 (
            echo 錯誤：無法安裝 pkg
            pause
            exit /b 1
        )
    )
)

REM 建立 dist 目錄
echo [2/5] 建立輸出目錄...
if not exist "dist" mkdir dist
if not exist "dist\data" mkdir dist\data

REM 複製必要檔案到 dist
echo [3/5] 複製資料檔案...
xcopy /Y /I "*.csv" "dist\" >nul 2>&1
xcopy /Y /I /E "public" "dist\public\" >nul 2>&1
if exist "data" xcopy /Y /I /E "data" "dist\data\" >nul 2>&1

REM 使用 pkg 打包
echo [4/5] 正在打包應用程式（這可能需要幾分鐘）...
echo.

REM 使用 npx 執行 pkg（最可靠的方式）
echo 使用 npx pkg 進行打包...
call npx pkg . --targets node18-win-x64 --output dist\newtaipei-address-lookup.exe

if errorlevel 1 (
    echo.
    echo ========================================
    echo 錯誤：打包失敗
    echo ========================================
    echo.
    echo 診斷資訊：
    echo - 檢查 Node.js 版本...
    call node --version
    echo.
    echo - 檢查 pkg 是否已安裝...
    if exist "node_modules\.bin\pkg.cmd" (
        echo   pkg.cmd 存在
    ) else if exist "node_modules\.bin\pkg" (
        echo   pkg 存在
    ) else (
        echo   pkg 不存在，嘗試重新安裝...
        call npm install pkg --save-dev
    )
    echo.
    echo 可能的原因：
    echo 1. Node.js 版本不符合（需要 Node.js 18 或以上）
    echo 2. 缺少必要的檔案（server.js 或 package.json）
    echo 3. 磁碟空間不足
    echo 4. 網路連線問題（pkg 需要下載 Node.js 二進位檔）
    echo.
    echo 建議解決方案：
    echo 1. 確認 Node.js 版本：node --version（應為 v18.x 或更高）
    echo 2. 手動執行：npm install pkg --save-dev
    echo 3. 然後執行：npx pkg . --targets node18-win-x64 --output dist\newtaipei-address-lookup.exe
    echo.
    pause
    exit /b 1
)

REM 建立啟動腳本
echo [5/5] 建立啟動腳本和說明文件...
(
echo @echo off
echo chcp 65001 ^>nul
echo cd /d "%%~dp0"
echo.
echo echo ========================================
echo echo 新北市地址查詢系統 - 可攜式版本
echo echo ========================================
echo echo.
echo echo 正在啟動服務...
echo echo 啟動後請在瀏覽器開啟: http://localhost:3000
echo echo 按 Ctrl+C 或關閉此視窗即可停止服務
echo echo.
echo newtaipei-address-lookup.exe
echo pause
) > dist\啟動服務.bat

REM 建立說明文件
(
echo # 新北市地址查詢系統 - 可攜式版本
echo.
echo ## 使用方式
echo.
echo 1. 雙擊「啟動服務.bat」啟動系統
echo 2. 在瀏覽器開啟 http://localhost:3000
echo 3. 開始查詢地址
echo.
echo ## 檔案說明
echo.
echo - `newtaipei-address-lookup.exe` - 主程式（不需要安裝 Node.js）
echo - `啟動服務.bat` - 啟動腳本
echo - `*.csv` - 門牌資料檔案
echo - `public\` - 網頁介面檔案
echo.
echo ## 注意事項
echo.
echo - 此版本為 Windows 64 位元版本
echo - 首次執行時，Windows 可能會顯示安全性警告，請選擇「仍要執行」
echo - 所有資料檔案都包含在此資料夾中，可整個資料夾複製到 USB 隨身碟使用
echo.
echo ## 系統需求
echo.
echo - Windows 7 或更新版本
echo - 不需要安裝 Node.js 或其他軟體
) > dist\README.txt

echo.
echo ========================================
echo 完成！
echo ========================================
echo.
echo 可攜式版本已建立於 dist 資料夾中
echo 您可以將 dist 資料夾複製到 USB 隨身碟或任何位置使用
echo.
echo 使用方式：
echo   1. 進入 dist 資料夾
echo   2. 雙擊「啟動服務.bat」
echo   3. 在瀏覽器開啟 http://localhost:3000
echo.
pause
