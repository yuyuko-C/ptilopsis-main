# -*- coding: utf-8 -*-
import traceback

from aiohttp.client_exceptions import ClientError
from nonebot.plugin import on_command, on_message
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent, Message
from nonebot.typing import T_State
from nonebot.plugin import require
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp.permission import *


from .saucenao import get_des as get_des_sau
from .ascii2d import get_des as get_des_asc

from src.utils.base.event_center import EventCenter
from src.utils.user_manager import UserManager
from src.utils.base.init_result import node_make,forward
from src.utils.base.api import send_group_forward_msg


__plugin_name__ = '搜图'



require_=require('nonebot_plugin_apsmatcher')
pic_command:Matcher=require_.pic_command


@pic_command.handle()
async def handle_first_receive(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg = str(event.message).strip()
    mode = state["_prefix"]["command"][0]
    state["mode"] = mode
    if mode == 'spi':
        if msg:
            state["arg"] = msg
        else:
            await pic_command.send('【以图搜图】你图呢？')
            pass
    elif mode == "spt":
        # await pic_command.send('请输入图片tag')
        await pic_command.finish('以tag搜图功能尚未开发')
        pass
    elif mode == "spa":
        # await pic_command.send('请输入画师名称')
        await pic_command.finish('以画师搜图功能尚未开发')
        pass



@pic_command.got("arg")
async def get_setu(bot: Bot, event: GroupMessageEvent, state: T_State):
    """
    发现没有的时候要发问
    :return:
    """
    try:
        mode = state["mode"]
        if mode == 'spi':
            await search_image(bot, event, state)
        elif mode == 'spt':
            await search_tag(bot, event, state)
        elif mode == 'spa':
            await search_artist(bot, event, state)

    except (IndexError, ClientError):
        await bot.send(event, traceback.format_exc())
        await pic_command.finish("参数错误")





async def search_image(bot: Bot, event: GroupMessageEvent, state: T_State):
 
    async def get_des(url:str):
        nodes = []
        
        async for msg in get_des_asc(url):
            if msg != None:
                nodes.append(node_make('梦中的樱雪',2648250775,msg))
        async for msg in get_des_sau(url):
            if msg != None:
                nodes.append(node_make('梦中的樱雪',2648250775,msg))
        if nodes:
            return forward(*nodes)
        else:
            return None
 
    msg: Message = Message(state["arg"])
    if msg[0].type == "image":
        await bot.send(event=event, message="正在解析图片特征信息")
        url = msg[0].data["url"]  # 图片链接
        forward_msg = await get_des(url)
        if forward_msg == None:
            await pic_command.finish('图片信息匹配失败，白面鸮未寻找到出处')
        else:
            await send_group_forward_msg(bot, event.group_id, forward_msg)

        await pic_command.finish('任务完成。博士，请为白面鸮本次的表现作出评价')
    else:
        await pic_command.finish("这不是图片,请不要把白面鸮当小孩子耍!")

async def search_artist(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg: Message = Message(state["arg"])
    if msg[0].type == "text":
        await bot.send(event=event, message="正在解析图片特征信息")
        url = msg[0].data["url"]  # 图片链接
        async for msg in get_des_sau(url):
            if msg==None:
                await pic_command.finish('图片信息匹配失败，白面鸮未寻找到出处')
            else:
                await bot.send(event=event, message=msg)
        # image_data: List[Tuple] = await get_pic_from_url(url)
        await pic_command.finish('任务完成。博士，请为白面鸮本次的表现作出评价')
    else:
        await pic_command.finish("这不是文字,请不要把白面鸮当小孩子耍!")

async def search_tag(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg: Message = Message(state["arg"])
    if msg[0].type == "text":
        await bot.send(event=event, message="正在解析图片特征信息")
        url = msg[0].data["url"]  # 图片链接
        async for msg in get_des_sau(url):
            if msg==None:
                await pic_command.finish('图片信息匹配失败，白面鸮未寻找到出处')
            else:
                await bot.send(event=event, message=msg)
        # image_data: List[Tuple] = await get_pic_from_url(url)
        await pic_command.finish('任务完成。博士，请为白面鸮本次的表现作出评价')
    else:
        await pic_command.finish("这不是文字,请不要把白面鸮当小孩子耍!")
