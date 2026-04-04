#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import os

def generate_minimal_cover():
    # 图片尺寸（微信公众号推荐 2.35:1）
    width = 900
    height = 383

    # 创建图片（浅色/白色背景）
    img = Image.new('RGB', (width, height), color='#ffffff')
    draw = ImageDraw.Draw(img)

    # 极简背景（白色）
    # 不做渐变，纯白

    # 极简几何装饰（深色圆形，和参考图一致）
    draw.ellipse(
        [150, 80, 250, 180],
        outline='#2c3e50',
        width=2
    )
    draw.ellipse(
        [width - 200, height - 140, width - 100, height - 40],
        outline='#2c3e50',
        width=2
    )

    # 中央文字：OAuth2
    try:
        font_paths = [
            '/System/Library/Fonts/Helvetica.ttc',
            '/System/Library/Fonts/SFNSDisplay.ttf',
            '/System/Library/Fonts/Arial.ttf',
        ]

        main_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                main_font = ImageFont.truetype(font_path, 72)
                break

        if main_font is None:
            main_font = ImageFont.load_default()

        # 主标题：OAuth2（深色）
        main_text = "OAuth2"
        main_bbox = draw.textbbox((0, 0), main_text, font=main_font)
        main_width = main_bbox[2] - main_bbox[0]
        main_height = main_bbox[3] - main_bbox[1]
        main_x = (width - main_width) // 2
        main_y = (height - main_height) // 2 - 20

        # 绘制文字（深灰色，和参考图一致）
        draw.text((main_x, main_y), main_text, fill='#2c3e50', font=main_font)

        # 副标题：OIDC（小字，深色）
        sub_font = None
        for font_path in font_paths:
            if os.path.exists(font_path):
                sub_font = ImageFont.truetype(font_path, 36)
                break

        if sub_font is None:
            sub_font = ImageFont.load_default()

        sub_text = "OIDC"
        sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        sub_width = sub_bbox[2] - sub_bbox[0]
        sub_x = (width - sub_width) // 2
        sub_y = main_y + main_height + 20

        draw.text((sub_x, sub_y), sub_text, fill='#34495e', font=sub_font)

    except Exception as e:
        print(f"Font error: {e}")

    # 底部装饰线（深色，和参考图一致）
    line_y = height - 60
    draw.line([350, line_y, 550, line_y], fill='#2c3e50', width=2)

    # 保存图片
    output_path = '/Users/yhzhu/project/blog/source/wechat-articles/images/iam-architecture/cover.png'
    img.save(output_path, 'PNG', quality=95)
    print(f"Minimal cover generated: {output_path}")

    return output_path

if __name__ == '__main__':
    generate_minimal_cover()
