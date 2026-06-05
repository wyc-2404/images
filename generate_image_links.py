#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成 GitHub 图片链接
支持三种格式：Raw、jsDelivr CDN、GitHub Pages
"""

import os

# ============ 配置区域 ============
USERNAME = "wyc-2024"
REPO = "images"
BRANCH = "main"
IMAGE_FOLDER = "downloaded_images"
# ==================================

def generate_links():
    """生成三种格式的图片链接"""
    
    # 检查文件夹是否存在
    folder_path = IMAGE_FOLDER
    if not os.path.exists(folder_path):
        print(f"错误：文件夹 '{folder_path}' 不存在！")
        print("请确保将图片放在 downloaded_images 文件夹中")
        return
    
    # 获取所有图片文件
    extensions = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp')
    images = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(extensions):
            images.append(filename)
    
    if not images:
        print(f"在 '{folder_path}' 中没有找到图片文件！")
        return
    
    # 排序保证顺序一致
    images.sort()
    
    # 生成三种格式的链接
    raw_links = []
    cdn_links = []
    pages_links = []
    
    for filename in images:
        # 1. Raw 链接
        raw_link = f"https://raw.githubusercontent.com/{USERNAME}/{REPO}/{BRANCH}/{IMAGE_FOLDER}/{filename}"
        raw_links.append(raw_link)
        
        # 2. jsDelivr CDN 链接
        cdn_link = f"https://cdn.jsdelivr.net/gh/{USERNAME}/{REPO}@{BRANCH}/{IMAGE_FOLDER}/{filename}"
        cdn_links.append(cdn_link)
        
        # 3. GitHub Pages 链接
        pages_link = f"https://{USERNAME}.github.io/{REPO}/{IMAGE_FOLDER}/{filename}"
        pages_links.append(pages_link)
    
    # 保存到文件
    with open("01_raw_links.txt", "w", encoding="utf-8") as f:
        f.write("# Raw 链接格式\n")
        f.write("# 格式：https://raw.githubusercontent.com/用户名/仓库/分支/路径/文件名\n")
        f.write("# 优点：无需认证，可直接访问\n")
        f.write("# 缺点：国内访问较慢\n\n")
        f.write("\n".join(raw_links))
    
    with open("02_cdn_links.txt", "w", encoding="utf-8") as f:
        f.write("# jsDelivr CDN 链接格式\n")
        f.write("# 格式：https://cdn.jsdelivr.net/gh/用户名/仓库@分支/路径/文件名\n")
        f.write("# 优点：全球CDN加速，国内访问快，自动压缩优化\n")
        f.write("# 缺点：需要公开仓库或带Token访问私有仓库\n\n")
        f.write("\n".join(cdn_links))
    
    with open("03_pages_links.txt", "w", encoding="utf-8") as f:
        f.write("# GitHub Pages 链接格式\n")
        f.write("# 格式：https://用户名.github.io/仓库/路径/文件名\n")
        f.write("# 优点：适合博客嵌入，稳定可靠\n")
        f.write("# 缺点：需要启用 GitHub Pages，仓库需公开\n")
        f.write("# 注意：需在仓库 Settings -> Pages 中启用 Pages\n\n")
        f.write("\n".join(pages_links))
    
    # 输出汇总
    print(f"✓ 共找到 {len(images)} 张图片")
    print(f"✓ 已生成 3 个链接文件：")
    print(f"  ├── 01_raw_links.txt（{len(raw_links)} 个链接）")
    print(f"  ├── 02_cdn_links.txt（{len(cdn_links)} 个链接）")
    print(f"  └── 03_pages_links.txt（{len(pages_links)} 个链接）")
    print(f"\n图片列表：")
    for i, img in enumerate(images, 1):
        print(f"  {i}. {img}")

if __name__ == "__main__":
    generate_links()
