# 新北市地址查詢系統

國外寄回台灣的信若少寫行政區，可輸入**路名**（以及選填的行政區、巷、弄、號），查詢該路名在新北市**可能所在的行政區**。

## 功能

- **輸入**：行政區（選填，可縮小範圍）、路名（必填）、巷、弄、號（選填）
- **輸出**：顯示「可能所在行政區」列表
- **PWA 支援**：可安裝到手機主畫面，像原生 APP 一樣使用

## 使用方式

### 本地開發

```bash
npm install
npm start
```

瀏覽器開啟：**http://localhost:3000**

### 部署到 Render

1. 將專案上傳到 GitHub
2. 在 Render 建立 Web Service
3. 連接 GitHub 專案
4. 設定：
   - Build Command: `npm install`
   - Start Command: `npm start`
   - Plan: Free
5. 部署完成後取得網址

### 手機使用

1. 在手機瀏覽器開啟網站
2. 安裝 PWA 到主畫面
3. 隨時可以使用，不需要電腦開著

## 技術

- 後端：Node.js + Express
- 前端：HTML、CSS、JavaScript（無框架）
- PWA：支援安裝到手機主畫面
- 資料來源：新北市各區門牌 CSV 資料

## 授權

MIT
