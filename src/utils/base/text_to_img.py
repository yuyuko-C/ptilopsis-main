from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import os


IMAGE_WIDTH=512

def __center_box(img:Image, background:Image):
    scale=0.7
    img_width=int(background.width*scale)
    img_height=int(background.height*scale)
    img.thumbnail((img_width,img_height))
    return background.width//2-img.width//2, background.height//2-img.height//2


def __text_to_img(text: str, texture:Image, font_color: tuple) :
    font_path = str(Path(__file__).parent.joinpath('default_font.otf'))
    if not os.path.exists(font_path):
        raise ValueError('Font not found')

    # 处理文字层 主体部分
    font_main_size = IMAGE_WIDTH // 25
    font_main = ImageFont.truetype(font_path, font_main_size)
    # 按长度切分文本
    spl_num = 0
    spl_list = []
    for num in range(len(text)):
        text_w = font_main.getsize_multiline(text[spl_num:num])[0]
        if text_w >= IMAGE_WIDTH * 0.78:
            spl_list.append(text[spl_num:num])
            spl_num = num
    else:
        spl_list.append(text[spl_num:])
    test_main_fin = '\n' + '\n'.join(spl_list) + '\n'

    # 绘制文字图层
    text_w, text_h = font_main.getsize_multiline(test_main_fin)
    text_main_img = Image.new(mode="RGBA", size=(text_w, text_h), color=(0, 0, 0, 0))
    ImageDraw.Draw(text_main_img).multiline_text(xy=(0, 0), text=test_main_fin, font=font_main, fill=font_color)

    # 初始化背景图层
    image_height = max(text_h + 50,IMAGE_WIDTH)
    background = Image.new(mode="RGB", size=(IMAGE_WIDTH, image_height), color=(255, 255, 255))
    # 向背景图层中置入贴图
    texture=texture.convert('RGBA')
    texture.putalpha(70)
    background.paste(im=texture, box=__center_box(texture,background),mask=texture)
    # 向背景图层中置入文字图层
    background.paste(im=text_main_img, box=(IMAGE_WIDTH // 10, max(image_height//2-text_h//2,25)), mask=text_main_img)


    return background


def text_to_img(text: str, texture_path:str, img_path:str, font_color: tuple = (140, 130, 130)) :
    FOLDER_PATH=Path(img_path).parent
    if not FOLDER_PATH.exists():
        FOLDER_PATH.mkdir(parents=True)

    byte_img = __text_to_img(text, Image.open(texture_path), font_color)
    # 保存图片
    byte_img.save(img_path, 'JPEG')
    return img_path


