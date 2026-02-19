# -*- coding: utf-8 -*-
"""
PWA 圖示生成工具
需要安裝 Pillow: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("請先安裝 Pillow: pip install Pillow")
    exit(1)

import os

def create_icon(size, output_path):
    """建立簡單的文字圖示"""
    # 建立圖片
    img = Image.new('RGB', (size, size), color='#58a6ff')
    draw = ImageDraw.Draw(img)
    
    # 繪製文字（簡化版，因為中文字體需要額外設定）
    # 這裡建立一個簡單的漸層圓形圖示
    center = size // 2
    radius = size // 2 - 10
    
    # 繪製圓形
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill='#388bfd',
        outline='#ffffff',
        width=3
    )
    
    # 儲存
    img.save(output_path, 'PNG')
    print(f"已建立: {output_path} ({size}x{size})")

def main():
    # 確保 public 資料夾存在
    public_dir = 'public'
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    
    # 建立圖示
    create_icon(192, os.path.join(public_dir, 'icon-192.png'))
    create_icon(512, os.path.join(public_dir, 'icon-512.png'))
    
    print("\n完成！圖示已建立於 public 資料夾")
    print("如果圖示不滿意，可以使用線上工具重新生成")

if __name__ == '__main__':
    main()
