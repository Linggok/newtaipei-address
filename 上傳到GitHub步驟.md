# 📤 上傳專案到 GitHub 步驟

## 前置準備

### 1. 安裝 Git（如果還沒有）

**檢查是否已安裝**：
```bash
git --version
```

**如果沒有安裝**：
1. 前往：https://git-scm.com/download/win
2. 下載並安裝 Git for Windows
3. 安裝時選擇預設選項即可

---

## 步驟 1：建立 GitHub 帳號

1. 前往：https://github.com
2. 點選「Sign up」
3. 填寫資料完成註冊
4. 驗證電子郵件

---

## 步驟 2：在 GitHub 建立新專案

1. 登入 GitHub
2. 點選右上角「+」→「New repository」
3. 填寫：
   - **Repository name**: `newtaipei-address`（或您喜歡的名稱）
   - **Description**: `新北市地址查詢系統`（選填）
   - **Public** 或 **Private**（選擇 Public 較簡單）
   - **不要**勾選「Initialize this repository with a README」
   - **不要**勾選「Add .gitignore」
   - **不要**選擇 License
4. 點選「Create repository」

---

## 步驟 3：在專案資料夾初始化 Git

開啟命令提示字元（PowerShell），執行：

```bash
cd c:\Users\user\Desktop\newtaipei
git init
```

---

## 步驟 4：建立 .gitignore

`.gitignore` 檔案已經建立好了，它會排除不必要的檔案（如 node_modules）。

確認檔案存在：
```bash
dir .gitignore
```

---

## 步驟 5：加入檔案到 Git

```bash
git add .
```

這會加入所有檔案到 Git（除了 .gitignore 中排除的）

---

## 步驟 6：提交檔案

```bash
git commit -m "Initial commit"
```

---

## 步驟 7：設定主分支名稱

```bash
git branch -M main
```

---

## 步驟 8：連接 GitHub 專案

**替換 `你的帳號` 為您的 GitHub 帳號名稱**：

```bash
git remote add origin https://github.com/你的帳號/newtaipei-address.git
```

例如，如果您的帳號是 `john123`，專案名稱是 `newtaipei-address`：
```bash
git remote add origin https://github.com/john123/newtaipei-address.git
```

---

## 步驟 9：上傳到 GitHub

```bash
git push -u origin main
```

**第一次上傳會要求登入**：
- 輸入您的 GitHub 帳號
- 輸入密碼（或 Personal Access Token）

**如果要求 Personal Access Token**：
1. 前往：https://github.com/settings/tokens
2. 點選「Generate new token (classic)」
3. 勾選 `repo` 權限
4. 產生 token
5. 複製 token（只會顯示一次）
6. 在密碼欄位貼上 token

---

## 步驟 10：確認上傳成功

1. 前往您的 GitHub 專案頁面
2. 應該可以看到所有檔案
3. 確認以下檔案存在：
   - `server.js`
   - `package.json`
   - `public/` 資料夾
   - `*.csv` 檔案（如果有的話）

---

## 完成！

現在您的專案已經在 GitHub 上了！

**下一步**：前往 Render 部署（參考 `Render部署完整步驟.md`）

---

## 疑難排解

### 問題：git 指令找不到

**解決**：安裝 Git for Windows（見步驟 1）

### 問題：要求 Personal Access Token

**解決**：建立 Personal Access Token（見步驟 9）

### 問題：上傳失敗

**檢查**：
- 確認 GitHub 專案名稱正確
- 確認帳號名稱正確
- 確認網路連線正常

### 問題：檔案太大無法上傳

**解決**：
- 確認 `.gitignore` 已排除 `node_modules/`
- 如果 CSV 檔案太大，可以考慮不提交（在 .gitignore 中加入 `*.csv`）

---

## 快速指令參考

```bash
# 初始化
git init

# 加入檔案
git add .

# 提交
git commit -m "Initial commit"

# 設定分支
git branch -M main

# 連接 GitHub
git remote add origin https://github.com/你的帳號/newtaipei-address.git

# 上傳
git push -u origin main
```

---

## 需要協助？

如果遇到問題，請告訴我：
1. 執行到哪個步驟
2. 出現什麼錯誤訊息

我會協助解決！
