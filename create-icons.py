# -*- coding: utf-8 -*-
"""
PWA Icon Generator
Requires Pillow: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Please install Pillow: pip install Pillow")
    exit(1)

import os

def create_icon(size, output_path):
    """Create a simple icon"""
    # Create image with blue background
    img = Image.new('RGB', (size, size), color='#58a6ff')
    draw = ImageDraw.Draw(img)
    
    # Draw a circle
    center = size // 2
    radius = size // 2 - 10
    
    # Draw outer circle
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill='#388bfd',
        outline='#ffffff',
        width=max(3, size // 64)
    )
    
    # Draw inner circle for depth
    inner_radius = radius - max(10, size // 10)
    draw.ellipse(
        [center - inner_radius, center - inner_radius, center + inner_radius, center + inner_radius],
        fill='#58a6ff',
        outline='#ffffff',
        width=max(2, size // 128)
    )
    
    # Save
    img.save(output_path, 'PNG')
    print(f"Created: {output_path} ({size}x{size})")

def main():
    # Ensure public directory exists
    public_dir = 'public'
    if not os.path.exists(public_dir):
        os.makedirs(public_dir)
    
    # Create icons
    create_icon(192, os.path.join(public_dir, 'icon-192.png'))
    create_icon(512, os.path.join(public_dir, 'icon-512.png'))
    
    print("\nDone! Icons created in public folder")
    print("You can replace these with custom icons later")

if __name__ == '__main__':
    main()
