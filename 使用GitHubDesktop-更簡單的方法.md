# 🎯 使用 GitHub Desktop - 更簡單的方法

## 為什麼使用 GitHub Desktop？

- ✅ **不需要命令列** - 全部用滑鼠點選
- ✅ **自動處理認證** - 不需要 Personal Access Token
- ✅ **視覺化操作** - 清楚看到每個步驟
- ✅ **錯誤提示清楚** - 知道哪裡出問題

---

## 📥 步驟 1：下載並安裝 GitHub Desktop

1. **前往**：https://desktop.github.com
2. **下載** GitHub Desktop for Windows
3. **安裝**（一直點 Next 即可）
4. **開啟** GitHub Desktop

---

## 🔐 步驟 2：登入 GitHub

1. **開啟** GitHub Desktop
2. **點選**「Sign in to GitHub.com」
3. **選擇**「Sign in with your browser」
4. **在瀏覽器中**：
   - 登入您的 GitHub 帳號（Linggok）
   - 授權 GitHub Desktop
5. **回到** GitHub Desktop，應該已經登入

---

## 📂 步驟 3：新增專案到 GitHub Desktop

### 方法 A：從現有資料夾新增（推薦）

1. **在 GitHub Desktop 中**：
   - 點選「File」→「Add Local Repository」
   - 或點選左上角「+」→「Add Existing Repository」

2. **選擇專案資料夾**：
   - 點選「Choose...」
   - 選擇：`C:\Users\user\Desktop\newtaipei`
   - 點選「Add repository」

3. **如果出現警告**：
   - 「This directory does not appear to be a Git repository」
   - 點選「create a repository」
   - Name: `newtaipei-address`
   - Description: `新北市地址查詢系統`（選填）
   - 點選「Create Repository」

---

## 📤 步驟 4：上傳到 GitHub

1. **在 GitHub Desktop 中**，您會看到：
   - 左側：變更的檔案列表
   - 下方：提交訊息欄位

2. **填寫提交訊息**：
   - 在下方輸入：`Initial commit`
   - 或使用預設訊息

3. **提交檔案**：
   - 點選左下角「Commit to main」
   - 等待完成

4. **發布到 GitHub**：
   - 點選右上角「Publish repository」
   - 或點選「Publish branch」（如果已經有 remote）
   - Repository name: `newtaipei-address`
   - Description: `新北市地址查詢系統`（選填）
   - **不要勾選**「Keep this code private」（除非您想要私人專案）
   - 點選「Publish Repository」

5. **等待上傳完成**
   - 會顯示進度
   - 完成後會顯示「Published」

---

## ✅ 步驟 5：確認上傳成功

1. **前往**：https://github.com/Linggok/newtaipei-address
2. **應該看到**：
   - ✅ 所有檔案都在
   - ✅ `server.js`
   - ✅ `package.json`
   - ✅ `public/` 資料夾
   - ✅ `*.csv` 檔案

---

## 🚀 步驟 6：部署到 Render

上傳成功後，前往 Render 部署：

1. **前往**：https://render.com
2. **登入**：使用 GitHub 帳號
3. **建立 Web Service**：
   - 點選「New +」→「Web Service」
   - 選擇 `Linggok/newtaipei-address`
   - 設定：
     - Build Command: `npm install`
     - Start Command: `npm start`
     - Plan: **Free**
   - 點選「Create Web Service」
4. **等待部署完成**
5. **取得網址**

---

## 🔧 疑難排解

### 問題：GitHub Desktop 無法登入

**解決方法**：
- 確認網路連線正常
- 嘗試使用瀏覽器登入 GitHub 確認帳號正常
- 清除 GitHub Desktop 的快取後重試

### 問題：找不到專案資料夾

**解決方法**：
- 確認資料夾路徑：`C:\Users\user\Desktop\newtaipei`
- 在檔案總管中確認資料夾存在

### 問題：發布失敗

**解決方法**：
- 確認 GitHub 帳號已登入
- 確認專案名稱沒有衝突
- 查看 GitHub Desktop 的錯誤訊息

### 問題：檔案沒有顯示

**解決方法**：
- 確認檔案確實存在於資料夾中
- 重新整理 GitHub Desktop（關閉後重新開啟）
- 確認檔案沒有被 .gitignore 排除

---

## 💡 優點

使用 GitHub Desktop 的優點：
- ✅ 不需要記指令
- ✅ 視覺化操作
- ✅ 自動處理認證
- ✅ 清楚看到變更
- ✅ 容易理解錯誤

---

## 📝 快速檢查清單

- [ ] GitHub Desktop 已安裝
- [ ] 已登入 GitHub 帳號
- [ ] 已新增專案到 GitHub Desktop
- [ ] 已提交檔案
- [ ] 已發布到 GitHub
- [ ] 在 GitHub 網站確認檔案已上傳
- [ ] 已部署到 Render

---

## 🆘 需要協助？

如果使用 GitHub Desktop 還是遇到問題，請告訴我：
1. 在哪個步驟失敗？
2. 看到什麼錯誤訊息？
3. GitHub Desktop 顯示什麼？

我會協助您解決！
