#!/usr/bin/env python3
"""
PWA Icon Generator for Orfe Admin Dashboard
Generates PNG icons from SVG logo in various sizes needed for PWA
"""

import os
from PIL import Image, ImageDraw, ImageFont
import requests

# Icon sizes needed for PWA
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

# Colors
BACKGROUND_COLOR = '#8BA888'
TEXT_COLOR = '#FFFFFF'

def create_icon(size):
    """Create a single icon of the specified size"""
    # Create image with background
    img = Image.new('RGBA', (size, size), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Add gradient effect (simplified)
    for i in range(size):
        alpha = int(255 * (1 - i / size * 0.2))
        color = (*tuple(int(BACKGROUND_COLOR[i:i+2], 16) for i in (1, 3, 5)), alpha)
        draw.rectangle([0, i, size, i+1], fill=color)
    
    # Add text
    try:
        # Try to use a bold font
        font_size_main = int(size * 0.2)
        font_size_sub = int(size * 0.12)
        
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
        # Main text "Orfe"
        text_main = "Orfe"
        bbox_main = draw.textbbox((0, 0), text_main, font=font_main)
        text_width_main = bbox_main[2] - bbox_main[0]
        text_height_main = bbox_main[3] - bbox_main[1]
        
        x_main = (size - text_width_main) // 2
        y_main = (size - text_height_main) // 2 - int(size * 0.05)
        
        draw.text((x_main, y_main), text_main, font=font_main, fill=TEXT_COLOR)
        
        # Sub text "Admin"
        text_sub = "Admin"
        bbox_sub = draw.textbbox((0, 0), text_sub, font=font_sub)
        text_width_sub = bbox_sub[2] - bbox_sub[0]
        
        x_sub = (size - text_width_sub) // 2
        y_sub = y_main + text_height_main + int(size * 0.05)
        
        draw.text((x_sub, y_sub), text_sub, font=font_sub, fill=TEXT_COLOR)
        
    except Exception as e:
        print(f"Font error for size {size}: {e}")
        # Fallback: just draw a circle
        margin = size // 4
        draw.ellipse([margin, margin, size-margin, size-margin], fill=TEXT_COLOR)
    
    return img

def generate_all_icons():
    """Generate all PWA icons"""
    icons_dir = '/var/Orfe-cosmatics/static/icons'
    
    # Ensure icons directory exists
    os.makedirs(icons_dir, exist_ok=True)
    
    print("Generating PWA icons...")
    
    for size in ICON_SIZES:
        try:
            icon = create_icon(size)
            filename = f'icon-{size}x{size}.png'
            filepath = os.path.join(icons_dir, filename)
            
            icon.save(filepath, 'PNG', quality=95)
            print(f"✓ Generated {filename}")
            
        except Exception as e:
            print(f"✗ Failed to generate icon for size {size}: {e}")
    
    print(f"\nAll icons saved to: {icons_dir}")

if __name__ == "__main__":
    generate_all_icons()
