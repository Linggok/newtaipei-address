# 🚀 部署到 Render - 詳細步驟

## ✅ 恭喜！GitHub 上傳成功

現在專案已經在 GitHub 上了：
👉 https://github.com/Linggok/newtaipei-address

下一步：部署到 Render，讓手機可以隨時使用（不需要電腦開著）！

---

## 📋 步驟 1：建立 Render 帳號

1. **前往**：https://render.com
2. **點選**：「Get Started for Free」
3. **選擇**：「Continue with GitHub」
4. **授權** Render 存取您的 GitHub 帳號
   - 會要求授權，點選「Authorize render」
   - 確認授權 Render 存取您的專案

---

## 📋 步驟 2：建立 Web Service

1. **登入後**，點選右上角「**New +**」
2. **選擇**：「**Web Service**」
3. **連接 GitHub 專案**：
   - 在「Connect a repository」中
   - 搜尋或選擇：`Linggok/newtaipei-address`
   - 如果沒看到，點選「**Configure account**」授權更多權限
   - 確認選擇正確的專案

---

## 📋 步驟 3：設定部署選項

填寫以下設定：

### 基本設定

- **Name**: `newtaipei-address`（或您喜歡的名稱）
- **Region**: 選擇離您最近的區域
  - 建議選擇：**Singapore**（亞洲，速度較快）
- **Branch**: `main`（預設，通常不需要改）
- **Root Directory**: **留空**（使用根目錄）

### 建置和啟動設定

- **Environment**: 選擇 **Node**
- **Build Command**: `npm install`
- **Start Command**: `npm start`
- **Plan**: 選擇 **Free**

### 進階設定（通常不需要改）

- Instance Type: 留預設
- Health Check Path: 留空
- Auto-Deploy: Yes（預設，自動部署）

---

## 📋 步驟 4：開始部署

1. **確認所有設定正確**
2. **點選**：「**Create Web Service**」
3. **等待部署**（約 2-5 分鐘）

---

## 📋 步驟 5：監控部署進度

部署過程中會顯示：

1. **Building**（建置中）
   - 執行 `npm install`
   - 安裝所有依賴

2. **Deploying**（部署中）
   - 啟動服務
   - 執行 `npm start`

3. **Live**（上線）
   - ✅ 部署完成！
   - 會顯示網址

---

## 📋 步驟 6：取得網址

部署完成後，您會看到：

- **URL**: `https://newtaipei-address.onrender.com`（或類似的網址）

**這就是您的手機可以使用的網址！**

---

## 📱 步驟 7：在手機上使用

### 7.1 開啟網站

1. **在手機瀏覽器開啟** Render 提供的網址
   - 例如：`https://newtaipei-address.onrender.com`

### 7.2 安裝 PWA

**Android（Chrome）**：
1. 點選右上角「⋮」（三個點）
2. 選擇「**安裝應用程式**」或「**新增至主畫面**」
3. 確認安裝

**iOS（Safari）**：
1. 點選下方「分享」按鈕（方框+箭頭）
2. 選擇「**加入主畫面**」
3. 確認加入

### 7.3 完成！

安裝後，手機主畫面上會出現「新北地址查詢」圖示，點擊即可使用！

---

## ⚠️ 重要提醒

### Render 免費方案限制

1. **休眠機制**：
   - 15 分鐘無活動後會休眠
   - 首次請求會較慢（約 30-60 秒喚醒）
   - 之後的請求會正常速度

2. **這是正常的**：
   - 免費方案的限制
   - 不影響使用，只是首次載入較慢

### 如果需要避免休眠

可以使用外部服務定期喚醒（例如：UptimeRobot），但這不是必須的。

---

## 🔧 疑難排解

### 問題：部署失敗

**可能原因**：
1. Build Command 或 Start Command 錯誤
2. Node.js 版本不符
3. 缺少依賴

**解決方法**：
- 確認 `package.json` 中的 `start` 腳本是 `node server.js`
- 確認 Node.js 版本 >= 18
- 查看 Render 的 **Logs** 分頁看錯誤訊息
- 確認所有 CSV 檔案都已上傳到 GitHub

### 問題：網站無法開啟

**可能原因**：
1. 部署還在進行中
2. Render 免費方案休眠

**解決方法**：
- 確認部署狀態是 **Live**
- 首次請求會較慢（喚醒需要時間），等待 30-60 秒
- 之後的請求會正常速度

### 問題：找不到專案

**解決方法**：
- 確認已授權 Render 存取 GitHub
- 點選「Configure account」授權更多權限
- 確認專案名稱正確：`Linggok/newtaipei-address`

---

## 📝 快速檢查清單

- [ ] Render 帳號已建立
- [ ] 已連接 GitHub 專案
- [ ] Web Service 已建立
- [ ] 設定正確（Build Command: `npm install`, Start Command: `npm start`）
- [ ] 部署狀態為 **Live**
- [ ] 取得 Render 網址
- [ ] 在手機瀏覽器測試網址
- [ ] 安裝 PWA 到主畫面
- [ ] 可以正常使用

---

## 🎉 完成！

部署完成後：
- ✅ 手機可以隨時使用
- ✅ 不需要電腦開著
- ✅ 可以分享給其他人
- ✅ 有固定的網址

---

## 🆘 需要協助？

如果部署時遇到問題，請告訴我：
1. 在哪個步驟失敗？
2. Render 顯示什麼錯誤訊息？
3. Logs 分頁顯示什麼？

我會協助您解決！
