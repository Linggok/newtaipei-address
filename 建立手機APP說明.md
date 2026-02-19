# 將系統做成手機 APP 的說明

## 方案一：PWA（Progressive Web App）- 推薦 ⭐

**優點**：
- ✅ 不需要重寫代碼
- ✅ 可以安裝到手機主畫面
- ✅ 支援 iOS 和 Android
- ✅ 不需要應用商店審核
- ✅ 更新方便（重新載入即可）

**已完成**：
- ✅ 已建立 `manifest.json`（應用程式設定檔）
- ✅ 已加入 PWA 安裝提示
- ✅ 已改進手機響應式設計
- ✅ 已加入 Service Worker（離線支援）

### 使用方式

#### 1. 啟動服務

```bash
npm start
```

#### 2. 在手機上開啟

- **Android**：
  1. 用 Chrome 瀏覽器開啟 `http://你的IP:3000`
  2. 點選瀏覽器選單（右上角三點）
  3. 選擇「安裝應用程式」或「新增至主畫面」
  4. 確認安裝

- **iOS**：
  1. 用 Safari 瀏覽器開啟 `http://你的IP:3000`
  2. 點選分享按鈕（下方中間）
  3. 選擇「加入主畫面」
  4. 確認加入

#### 3. 從手機主畫面開啟

安裝後，手機主畫面上會出現「新北地址查詢」圖示，點擊即可開啟。

### 需要建立的圖示

PWA 需要圖示檔案，請建立以下檔案（或使用線上工具生成）：

1. `public/icon-192.png` - 192x192 像素
2. `public/icon-512.png` - 512x512 像素

**快速生成圖示**：
- 使用 [PWA Asset Generator](https://github.com/onderceylan/pwa-asset-generator)
- 或使用 [RealFaviconGenerator](https://realfavicongenerator.net/)

### 部署到網際網路

要讓手機可以安裝，需要將服務部署到網際網路：

**選項 1：使用 ngrok（測試用）**
```bash
npm install -g ngrok
ngrok http 3000
```
會得到一個公開網址，例如：`https://xxxx.ngrok.io`

**選項 2：部署到雲端服務**
- Vercel
- Heroku
- Railway
- Render
- 或任何支援 Node.js 的服務

---

## 方案二：使用 Capacitor（原生 APP）

如果需要更完整的原生功能（推播通知、相機等），可以使用 Capacitor：

### 安裝 Capacitor

```bash
npm install @capacitor/core @capacitor/cli
npm install @capacitor/ios @capacitor/android
npx cap init
```

### 建立 iOS APP

```bash
npx cap add ios
npx cap sync
npx cap open ios
```

### 建立 Android APP

```bash
npx cap add android
npx cap sync
npx cap open android
```

### 打包成 APK/IPA

需要安裝：
- Android Studio（Android）
- Xcode（iOS，僅 macOS）

---

## 方案三：使用 React Native（完全重寫）

如果需要完全原生的體驗，可以考慮用 React Native 重寫前端，但需要較多時間。

---

## 目前推薦：PWA

對於您的需求，**PWA 是最佳選擇**，因為：
1. 不需要重寫代碼
2. 可以安裝到手機主畫面
3. 使用體驗接近原生 APP
4. 更新方便

### 下一步

1. **建立圖示**：使用線上工具生成 `icon-192.png` 和 `icon-512.png`
2. **測試 PWA**：在手機瀏覽器開啟並測試安裝
3. **部署服務**：使用 ngrok 或雲端服務讓手機可以存取

### 測試清單

- [ ] 在手機瀏覽器開啟網站
- [ ] 檢查是否顯示「安裝應用程式」提示
- [ ] 安裝到主畫面
- [ ] 從主畫面開啟應用程式
- [ ] 測試所有功能是否正常運作
- [ ] 檢查響應式設計（手機橫向/直向）

---

## 疑難排解

**Q: 手機上看不到安裝提示？**
A: 
- 確認使用 HTTPS（或 localhost）
- 確認 manifest.json 正確載入
- 檢查瀏覽器是否支援 PWA

**Q: 圖示顯示不正確？**
A: 
- 確認圖示檔案路徑正確
- 確認圖示尺寸符合要求
- 清除瀏覽器快取後重試

**Q: Service Worker 無法註冊？**
A: 
- 確認使用 HTTPS（或 localhost）
- 檢查 service-worker.js 檔案是否存在
- 查看瀏覽器控制台的錯誤訊息
