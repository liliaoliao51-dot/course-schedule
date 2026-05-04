#!/usr/bin/env python3
"""
生成 PWA 图标的脚本
设计风格：现代、冷淡、极简
"""

from PIL import Image, ImageDraw
import os

def create_icon(size, output_path):
    """创建极简风格的课表图标"""

    # 创建图像
    img = Image.new('RGB', (size, size), '#2d2d2d')  # 深灰色背景
    draw = ImageDraw.Draw(img)

    # 计算边距和单元格大小
    margin = size * 0.2
    grid_size = size - 2 * margin
    cell_size = grid_size / 4  # 4x4 网格表示课表

    # 绘制网格线（白色，细线条）
    line_width = max(2, size // 100)
    line_color = 'white'

    # 垂直线
    for i in range(5):
        x = margin + i * cell_size
        draw.line([(x, margin), (x, size - margin)], fill=line_color, width=line_width)

    # 水平线
    for i in range(5):
        y = margin + i * cell_size
        draw.line([(margin, y), (size - margin, y)], fill=line_color, width=line_width)

    # 添加一些"课程块"（半透明白色填充）
    # 使用圆角矩形模拟课程块
    block_padding = size * 0.02
    block_radius = size * 0.03

    # 课程块位置 (行, 列)
    blocks = [
        (0, 0, 2, 1),  # 第1-2节，周一
        (1, 1, 1, 2),  # 第3节，周二-周三
        (2, 2, 1, 1),  # 第5节，周三
        (3, 0, 1, 1),  # 第7节，周一
        (0, 3, 1, 1),  # 第1节，周四
    ]

    # 浅灰色填充课程块
    block_color = (255, 255, 255, 60)  # 半透明白色

    # 创建一个带透明度的图层用于课程块
    overlay = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)

    for row, col, rowspan, colspan in blocks:
        x1 = margin + col * cell_size + block_padding
        y1 = margin + row * cell_size + block_padding
        x2 = margin + (col + colspan) * cell_size - block_padding
        y2 = margin + (row + rowspan) * cell_size - block_padding

        # 绘制圆角矩形
        overlay_draw.rounded_rectangle(
            [x1, y1, x2, y2],
            radius=block_radius,
            fill=block_color
        )

    # 合并图层
    img = Image.alpha_composite(img.convert('RGBA'), overlay)

    # 保存
    img.save(output_path, 'PNG')
    print(f"已生成: {output_path}")

def main():
    # 确保目录存在
    icons_dir = os.path.join(os.path.dirname(__file__), 'public', 'icons')
    os.makedirs(icons_dir, exist_ok=True)

    # 生成两种尺寸
    create_icon(512, os.path.join(icons_dir, 'logo-512.png'))
    create_icon(192, os.path.join(icons_dir, 'logo-192.png'))

    print("\n图标生成完成！")
    print(f"文件位置: {icons_dir}")

if __name__ == '__main__':
    main()
