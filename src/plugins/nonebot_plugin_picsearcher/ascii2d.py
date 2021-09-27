# -*- coding: utf-8 -*-
from typing import List, Tuple
from urllib.parse import urljoin
import aiofiles
from src.config.path import PROXY
from asyncio.exceptions import TimeoutError
from src.utils.base.init_result import image

from lxml.html import fromstring
import aiohttp


def parse_html(html: str):
    selector = fromstring(html)
    for tag in selector.xpath('//div[@class="container"]/div[@class="row"]/div/div[@class="row item-box"]')[1:5]:
        if pic_url := tag.xpath('./div/img[@loading="lazy"]/@src'):  # 缩略图url
            pic_url = urljoin("https://ascii2d.net/", pic_url[0])
        if description := tag.xpath('./div/div/h6/a[1]/text()'):  # 名字
            description = description[0]
        if author := tag.xpath('./div/div/h6/a[2]/text()'):  # 作者
            author = author[0]
        if origin_url := tag.xpath('./div/div/h6/a[1]/@href'):  # 原图地址
            origin_url = origin_url[0]
        if author_url := tag.xpath('./div/div/h6/a[2]/@href'):  # 作者地址
            author_url = author_url[0]
        yield pic_url, description, author, origin_url, author_url

    pass


async def get_pic_from_url(url: str):
    real_url = "https://ascii2d.net/search/url/" + url
    async with aiohttp.ClientSession() as session:
        async with session.get(real_url, proxy=PROXY) as resp:
            html: str = await resp.text()
        return [i for i in parse_html(html)]


async def get_des(url: str):
    image_data: List[Tuple] = await get_pic_from_url(url)
    if not image_data:
        yield 
    for pic in image_data:
        msg = f"标题：{pic[2]}({pic[1]})\n"
        msg += image(img_name=pic[0])+"\n"
        msg += f"来源：{pic[3]}"
        yield msg
