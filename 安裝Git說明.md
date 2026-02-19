# 安裝 Git 說明

## 問題

系統顯示：`git : The term 'git' is not recognized`

這表示您的電腦還沒有安裝 Git。

---

## 解決方案：安裝 Git for Windows

### 步驟 1：下載 Git

1. 前往：https://git-scm.com/download/win
2. 會自動開始下載（約 50MB）
3. 或點選「Click here to download」手動下載

### 步驟 2：安裝 Git

1. **執行下載的安裝檔**（例如：`Git-2.xx.x-64-bit.exe`）

2. **安裝選項**（建議使用預設值）：
   - ✅ 一直點「Next」使用預設選項即可
   - ✅ 確認勾選「Git Bash Here」和「Git GUI Here」
   - ✅ 確認勾選「Add a Git Bash profile to Windows Terminal」（如果有）

3. **完成安裝**
   - 點選「Finish」

### 步驟 3：重新開啟命令提示字元

**重要**：安裝 Git 後，需要**重新開啟**命令提示字元（或 PowerShell），Git 才會生效。

1. 關閉目前的命令提示字元視窗
2. 重新開啟命令提示字元（或 PowerShell）

### 步驟 4：確認 Git 已安裝

在新的命令提示字元中執行：

```bash
git --version
```

**應該看到**：
```
git version 2.xx.x
```

如果看到版本號碼，表示 Git 安裝成功！

---

## 安裝完成後，執行您的指令

安裝 Git 並重新開啟命令提示字元後，執行：

```bash
cd c:\Users\user\Desktop\newtaipei
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Linggok/newtaipei-address.git
git push -u origin main
```

---

## 快速安裝連結

**直接下載**：
- https://git-scm.com/download/win

**安裝時間**：約 2-3 分鐘

---

## 安裝後可能需要的設定

### 設定使用者名稱和電子郵件（第一次使用時）

Git 可能會要求設定：

```bash
git config --global user.name "您的名稱"
git config --global user.email "您的email@example.com"
```

例如：
```bash
git config --global user.name "Linggok"
git config --global user.email "your-email@example.com"
```

---

## 替代方案：使用 GitHub Desktop（圖形介面）

如果您不喜歡命令列，可以使用 GitHub Desktop：

1. **下載**：https://desktop.github.com
2. **安裝並登入** GitHub 帳號
3. **新增專案**：
   - File → Add Local Repository
   - 選擇 `C:\Users\user\Desktop\newtaipei`
4. **發布到 GitHub**：
   - 點選「Publish repository」
   - 輸入專案名稱：`newtaipei-address`
   - 確認勾選「Keep this code private」（如果需要）
   - 點選「Publish Repository」

---

## 需要協助？

安裝 Git 後，如果遇到問題，請告訴我：
1. Git 是否安裝成功？（執行 `git --version` 的結果）
2. 執行指令時出現什麼錯誤訊息？

我會協助您完成上傳！
