# PWA 圖示建立說明

PWA 需要兩個圖示檔案才能正常運作：
- `public/icon-192.png` (192x192 像素)
- `public/icon-512.png` (512x512 像素)

## 方法一：使用線上工具（最簡單）

1. 前往 [PWA Asset Generator](https://github.com/onderceylan/pwa-asset-generator)
   - 或直接使用：https://www.pwabuilder.com/imageGenerator

2. 上傳一張圖片（建議至少 512x512）

3. 下載生成的圖示

4. 將 `icon-192.png` 和 `icon-512.png` 放到 `public` 資料夾

## 方法二：使用 Python 腳本（如果有圖片）

如果您有原始圖片，可以使用以下 Python 腳本：

```python
from PIL import Image

# 讀取原始圖片
img = Image.open('原始圖片.png')

# 生成 192x192
icon_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
icon_192.save('public/icon-192.png')

# 生成 512x512
icon_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
icon_512.save('public/icon-512.png')
```

## 方法三：使用簡單的 SVG 轉換

如果暫時沒有圖示，可以使用文字圖示：

1. 建立一個簡單的 HTML 檔案，用 Canvas 繪製圖示
2. 或使用線上工具如 [Canva](https://www.canva.com/) 建立簡單圖示

## 快速測試（暫時跳過圖示）

如果暫時沒有圖示檔案，PWA 仍然可以運作，只是：
- 安裝時可能沒有圖示顯示
- 主畫面上可能顯示預設圖示

您可以先測試功能，之後再補上圖示。
