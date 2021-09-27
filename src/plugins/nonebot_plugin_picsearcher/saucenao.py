# -*- coding: utf-8 -*-
import io
from typing import List, Tuple

import aiohttp
from lxml.html import fromstring
from src.utils.base.init_result import image


from .formdata import FormData


header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryPpuR3EZ1Ap2pXv8W",
    'Connection': 'keep-alive',
    'Host': 'saucenao.com', 'Origin': 'https://saucenao.com', 'Referer': 'https://saucenao.com/index.php',
    'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}



def parse_html(html: str):
    """
    解析nao返回的html
    :param html:
    :return:
    """
    selector = fromstring(html)
    for tag in selector.xpath('//div[@class="result"]/table'):
        pic_url = tag.xpath('./tr/td/div/a/img/@src')
        if pic_url:
            pic_url = pic_url[0]
        else:
            pic_url = None  # 图片源
        xsd: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultmatchinfo"]/div[@class="resultsimilarityinfo"]/text()')
        if xsd:
            xsd = xsd[0]
        else:
            xsd = "信息缺失"  # 相似度
        strong_text = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resulttitle"]/strong/text()')
        plain_text = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resulttitle"]/text()')
        title: List[str] = plain_text if plain_text else strong_text
        if title:
            title = title[0]
        else:
            title = "信息缺失"  # 标题
        # pixiv id
        pixiv_id: List[str] = tag.xpath(
            './tr/td[@class="resulttablecontent"]/div[@class="resultcontent"]/div[@class="resultcontentcolumn"]/a[1]/@href')
        if pixiv_id:
            pixiv_id = pixiv_id[0]
        else:
            pixiv_id = "信息缺失"
        yield pic_url, xsd, title, pixiv_id



async def get_pic_from_url(url: str):
    """
    从url搜图
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            content = io.BytesIO(await resp.read())
        data = FormData(boundary="----WebKitFormBoundaryPpuR3EZ1Ap2pXv8W")
        data.add_field(name="file", value=content, content_type="image/jpeg",
                       filename="blob")
        async with session.post("https://saucenao.com/search.php", data=data, headers=header) as res:
            html = await res.text()
            image_data = [each for each in parse_html(html) if each[0]!=None and float(each[1].strip('%'))>90]
            image_data = image_data[:3]
    return image_data


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        yield
    for pic in image_data:
        msg = f"标题：{pic[2]}({pic[1]})\n"
        msg += image(img_name=pic[0])+"\n"
        msg += f"来源：{pic[3]}"
        yield msg
    pass

