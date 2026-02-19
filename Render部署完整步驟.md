# 🚀 Render 部署完整步驟

## 前置準備

### 1. 建立 GitHub 帳號（如果還沒有）

1. 前往：https://github.com
2. 點選「Sign up」註冊
3. 完成註冊流程

### 2. 將專案上傳到 GitHub

#### 步驟 A：初始化 Git（如果還沒有）

開啟命令提示字元，執行：

```bash
cd c:\Users\user\Desktop\newtaipei
git init
```

#### 步驟 B：建立 .gitignore（避免上傳不必要的檔案）

建立 `.gitignore` 檔案，內容：

```
node_modules/
dist/
.env
*.log
.DS_Store
```

#### 步驟 C：提交檔案到 Git

```bash
git add .
git commit -m "Initial commit"
git branch -M main
```

#### 步驟 D：在 GitHub 建立新專案

1. 前往：https://github.com/new
2. Repository name: `newtaipei-address`（或您喜歡的名稱）
3. 選擇 Public 或 Private
4. **不要**勾選「Initialize this repository with a README」
5. 點選「Create repository」

#### 步驟 E：上傳到 GitHub

GitHub 會顯示指令，執行：

```bash
git remote add origin https://github.com/你的帳號/newtaipei-address.git
git push -u origin main
```

（把 `你的帳號` 換成您的 GitHub 帳號名稱）

---

## Render 部署步驟

### 步驟 1：建立 Render 帳號

1. 前往：https://render.com
2. 點選「Get Started for Free」
3. 選擇「Continue with GitHub」
4. 授權 Render 存取您的 GitHub 帳號

### 步驟 2：建立 Web Service

1. 登入後，點選右上角「New +」
2. 選擇「**Web Service**」

### 步驟 3：連接 GitHub 專案

1. 在「Connect a repository」中，選擇您的專案（`newtaipei-address`）
2. 如果沒看到，點選「Configure account」授權更多權限

### 步驟 4：設定部署選項

填寫以下設定：

- **Name**: `newtaipei-address`（或您喜歡的名稱）
- **Region**: 選擇離您最近的區域（例如：Singapore）
- **Branch**: `main`（預設）
- **Root Directory**: 留空（使用根目錄）
- **Environment**: `Node`
- **Build Command**: `npm install`
- **Start Command**: `npm start`
- **Plan**: 選擇 **Free**

### 步驟 5：設定環境變數（如果需要）

如果您的應用程式需要環境變數（例如 `NTPC_DATASET_OID`）：

1. 在部署設定頁面，找到「Environment Variables」
2. 點選「Add Environment Variable」
3. 輸入變數名稱和值
4. 點選「Save Changes」

### 步驟 6：開始部署

1. 確認所有設定正確
2. 點選「Create Web Service」
3. Render 會開始部署（約 2-5 分鐘）

### 步驟 7：等待部署完成

部署過程中會顯示：
- Building（建置中）
- Deploying（部署中）
- Live（上線）

### 步驟 8：取得網址

部署完成後，您會看到：
- **URL**: `https://newtaipei-address.onrender.com`（或類似的網址）

**這就是您的手機可以使用的網址！**

---

## 部署後的使用

### 在手機上使用

1. **在手機瀏覽器開啟**：
   ```
   https://newtaipei-address.onrender.com
   ```
   （替換成您的實際網址）

2. **安裝 PWA**：
   - **Android（Chrome）**：
     - 點選右上角「⋮」
     - 選擇「安裝應用程式」或「新增至主畫面」
   - **iOS（Safari）**：
     - 點選下方「分享」按鈕
     - 選擇「加入主畫面」

3. **完成！**
   - ✅ 不需要電腦開著
   - ✅ 隨時可以使用
   - ✅ 可以分享給其他人

---

## 注意事項

### Render 免費方案限制

1. **休眠機制**：
   - 15 分鐘無活動後會休眠
   - 首次請求會較慢（約 30-60 秒喚醒）
   - 之後的請求會正常速度

2. **解決休眠問題**：
   - 使用 Render 的「Always On」功能（需要付費）
   - 或使用外部服務定期喚醒（例如：UptimeRobot）

### 更新應用程式

當您更新程式碼後：

1. 提交到 GitHub：
   ```bash
   git add .
   git commit -m "Update"
   git push
   ```

2. Render 會自動偵測並重新部署

---

## 疑難排解

### 問題：部署失敗

**檢查**：
- 確認 `package.json` 中的 `start` 腳本正確
- 確認 Node.js 版本符合要求（>=18）
- 查看 Render 的部署日誌（Logs）

### 問題：網站無法開啟

**檢查**：
- 確認服務已部署完成（狀態為 Live）
- 確認網址正確
- 查看 Render 的日誌是否有錯誤

### 問題：首次載入很慢

**原因**：Render 免費方案會休眠，首次請求需要喚醒

**解決**：
- 這是正常的，等待 30-60 秒即可
- 之後的請求會正常速度

---

## 進階設定

### 自訂網址

Render 免費方案提供：
- 預設網址：`https://newtaipei-address.onrender.com`
- 可以自訂子網域：`https://newtaipei-address.onrender.com`

### 設定自動部署

Render 預設會自動部署：
- 當您 push 到 GitHub 時
- Render 會自動偵測並重新部署

### 查看日誌

1. 在 Render 專案頁面
2. 點選「Logs」分頁
3. 可以查看即時日誌

---

## 完成！

現在您的應用程式已經部署到 Render，手機可以隨時使用，不需要電腦開著！

**下一步**：
1. 在手機瀏覽器開啟 Render 提供的網址
2. 安裝 PWA 到主畫面
3. 開始使用！

---

## 需要協助？

如果遇到問題，請告訴我：
1. 執行到哪個步驟
2. 出現什麼錯誤訊息
3. Render 日誌顯示什麼

我會協助解決！
