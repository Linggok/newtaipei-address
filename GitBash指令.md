# Git Bash 正確指令

## 問題

Git Bash 使用 Unix 風格的路徑，Windows 路徑格式不適用。

## 正確的 Git Bash 指令

### 方法 1：使用 Unix 風格路徑

```bash
cd /c/Users/user/Desktop/newtaipei
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Linggok/newtaipei-address.git
git push -u origin main
```

### 方法 2：使用相對路徑（如果在 Desktop）

```bash
cd ~/Desktop/newtaipei
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Linggok/newtaipei-address.git
git push -u origin main
```

### 方法 3：直接從專案資料夾開啟 Git Bash（最簡單）

1. 在檔案總管中，前往 `C:\Users\user\Desktop\newtaipei`
2. 在資料夾空白處，**右鍵點選**
3. 選擇「**Git Bash Here**」
4. Git Bash 會自動開啟，位置已經是專案資料夾
5. 直接執行：

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/Linggok/newtaipei-address.git
git push -u origin main
```

---

## 路徑轉換說明

| Windows 路徑 | Git Bash 路徑 |
|-------------|--------------|
| `c:\Users\user\Desktop\newtaipei` | `/c/Users/user/Desktop/newtaipei` |
| `C:\Users\user\Desktop\newtaipei` | `/c/Users/user/Desktop/newtaipei` |

**規則**：
- `c:\` → `/c/`
- `\` → `/`
- 路徑不區分大小寫

---

## 確認位置正確

執行以下指令確認：

```bash
pwd
```

**應該顯示**：
```
/c/Users/user/Desktop/newtaipei
```

然後執行：

```bash
ls
```

**應該看到**：
- `server.js`
- `package.json`
- `public/`
- `*.csv` 檔案
- 等等...

---

## 完整指令（Git Bash）

```bash
# 切換到專案資料夾
cd /c/Users/user/Desktop/newtaipei

# 確認位置
pwd

# 確認檔案
ls

# 加入檔案
git add .

# 提交
git commit -m "Initial commit"

# 設定主分支
git branch -M main

# 連接 GitHub
git remote add origin https://github.com/Linggok/newtaipei-address.git

# 上傳
git push -u origin main
```

---

## 推薦方法

**最簡單**：在專案資料夾中右鍵 → 「Git Bash Here」，然後直接執行 Git 指令（不需要 cd）。
