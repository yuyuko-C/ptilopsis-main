import random
import json
import re
import asyncio
from datetime import datetime,timedelta,date
from functools import wraps

from PIL import Image
from aiohttp.client_exceptions import ClientError
from pixivpy_async import *

from nonebot.adapters.cqhttp.bot import Bot
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import GroupMessageEvent
from nonebot.typing import T_State
from nonebot.exception import IgnoredException
from pixivpy_async.error import RetryExhaustedError

from src.utils.logger_manager import LoggerManger,Logger
from src.utils.group_manager import GroupManager,Group
from src.utils.user_manager import UserManager
from src.utils.logger_manager.model import Chat_Message
from src.utils.base.api import *
from src.utils.base.init_result import *
from src.config import doc, path, _REFRESH_TOKEN



# BASE#


async def loadInfo(bot:Bot):

    #
    user_id_list=[]
    group_id_list=[]

    #读取在线信息
    group_list = await get_group_list(bot)
    group_id_list.extend([int(group['group_id']) for group in group_list])
    for group in group_list:
        group_id = int(group['group_id'])
        group_member_list = await get_group_member_list(bot, group_id)
        user_id_list.extend([int(memeber['user_id']) for memeber in group_member_list])
        g = GroupManager.getGroup(group_id)
        g.nickname = group['group_name']
        g.members = group_member_list
        #载入本地不存在的用户信息
        for memeber in group_member_list:
            user_id = int(memeber['user_id'])
            user = UserManager.getUser(user_id)
            user.nick_name = memeber['nickname']   
            # print(len(UserManager._register))

    #清除多余的用户信息
    register_users = UserManager._register.copy()
    for reg_user_id in register_users:
        if reg_user_id not in user_id_list:
            del UserManager._register[reg_user_id]

    #清除多余的群信息
    register_groups = GroupManager._register.copy()
    for reg_group_id in register_groups:
        if reg_group_id not in group_id_list:
            del GroupManager._register[reg_group_id]

async def clean_image_file():
    clean_folder = os.path.abspath('./go-cqhttp/data/images')
    necessary = []

    query = Chat_Message.select(Chat_Message.plain_text).tuples()
    for text in query:
        match = re.search(r'\[CQ:image,file=(.+)\]',text[0])
        if match:
            file_name = match.group(1)
            necessary.append(file_name)

    file_list = os.listdir(clean_folder)
    [os.remove(os.path.join(clean_folder,file_name)) for file_name in file_list if file_name not in necessary]




# PIXIV #
retryable_error = (ConnectionResetError,ClientError,ConnectionError)
class AppPixiv:
    
    def __init__(self,aapi:AppPixivAPI) -> None:
        aapi.set_accept_language('zh')
        self.aapi = aapi

        # 读取本地的pixiv排行信息
        if os.path.exists(path.ILLUSTION_PATH):
            with open(path.ILLUSTION_PATH,'r') as f:
                local_rankinfo = json.load(f)['info']

        self.local_rankinfo = local_rankinfo if local_rankinfo else {}

        pass

    def need_update(self):
        old_urllist=[img['download_url'] for img in self.local_rankinfo]
        new_urllist=[img['download_url'] for img in self.new_rankinfo]
        return old_urllist != new_urllist


    @retry(*retryable_error,retries=5,cooldown=60*3)
    async def login(self):
        await self.aapi.login(refresh_token=_REFRESH_TOKEN)

    @retry(*retryable_error,retries=5,cooldown=60*3)
    async def get_new_rankinfo(self,date:str=None):

        rank_info = (await self.aapi.illust_ranking(date=date))['illusts']

        for index,img in enumerate(rank_info) :
            # print(img['title'],img['sanity_level'])
            original_url = img.meta_single_page.original_image_url if img.meta_single_page else img.meta_pages[0].image_urls.original
            large_url = img.image_urls.large
            img['download_url'] = large_url
            img['file_name'] = 'Rank{}.jpg'.format(index)
            img['file_path'] = os.path.join(path.DAILYRANK_FOLDER_PATH, img['file_name'])

        self.new_rankinfo = rank_info

    @retry(*retryable_error,retries=5,cooldown=60*3)
    async def download(self,img:dict):
        await self.aapi.download(img['download_url'],fname = open(img['file_path'], 'wb'))
        im = Image.open(img['file_path']).convert("RGB")
        im.save(img['file_path'], "JPEG")



illusts = {'info':{}}

async def dowanloadPixivRank(bot:Bot):

    try:

        async with PixivClient(proxy=path.PROXY) as client:
            aapi = AppPixiv(AppPixivAPI(client=client))
            log.info('正在登录P站');await aapi.login()
            log.info('正在获取P站排行');await aapi.get_new_rankinfo(str(date.today()-timedelta(2)))
            
            if aapi.need_update():
                log.info('正在更新P站排行')
                for index,img in enumerate(aapi.new_rankinfo) :
                    await aapi.download(img)
                    print('已更新：',index, img['download_url'])

                # 下载完成，保存当前排行榜信息到本地
                illusts['info'] = aapi.new_rankinfo
                with open(path.ILLUSTION_PATH,'w') as f:
                    json.dump(illusts,f)
                    log.info('{}P站更新完成'.format(date.today()))
                    await send_private_msg(bot,1061439585,None,'P站更新完成-{}'.format(date.today()))
            else:
                log.info('P站日榜无需更新')
                await send_private_msg(bot,1061439585,None,'P站日榜无需更新-{}'.format(date.today()))

    except RetryExhaustedError:
        log.info('{}P站连接失败'.format(date.today()))
        await send_private_msg(bot,1061439585,None,'P站连接失败-{}'.format(date.today()))





# EVENT_CENTER #


async def logCreateCallback(bot: Bot, event: GroupMessageEvent, state: T_State, matcher:Matcher):
    #更新记录图片
    log.info('更新记录图片')
    LoggerManger.updateLogListImage(event.group_id)
    #发布公告
    log.info('发布公告')
    logger:Logger = state['logger']
    if not logger.private:
        for group_id in GroupManager._register:
            group = GroupManager.getGroup(group_id)
            if (group_id != event.group_id) and group.send_message:
                msg = text('白面鸮检测到新的记录\n标题:{}'.format(logger.title))
                await send_group_msg(bot, group_id, msg)
            else:
                await send_group_msg(bot, group_id, text('记录已同步至其他群聊。'))
    pass


async def logSeeCallback(bot: Bot, event: GroupMessageEvent, state: T_State, matcher:Matcher):
    pass


async def getFeatherCallback(bot: Bot, event: GroupMessageEvent, state: T_State, matcher:Matcher):

    user = UserManager.getUser(event.user_id)
    feather_num = int(state['value'])

    level = user.getPotentialLevel()
    user.feathers += feather_num

    if level < user.getPotentialLevel():
        await matcher.send('潜能已升级')

    await matcher.send(text('{} [ 灰羽+{} ] '.format(random.choice(doc.LINES_CLOSE), feather_num))+at(event.user_id))

    pass


async def triggerPlugin(bot: Bot, event: GroupMessageEvent, state: T_State, matcher:Matcher):
    scheduler = state['scheduler']
    
    user = UserManager.getUser(event.user_id)
    user.trigger_times += 1

    run_date=datetime.now() + timedelta(minutes=1)
    @scheduler.scheduled_job("date" ,run_date = run_date)
    async def decrease_times():
        user.trigger_times -= 1

    if user.trigger_times > 7:
        await send_group_msg(bot,event.group_id,at(event.user_id)+text('别再骚扰我了，屑！博！士！ 不理你了，哼！'))
        UserManager.blacklistUser(event.user_id)
        
        run_date=datetime.now()+timedelta(minutes=20)
        @scheduler.scheduled_job("date",run_date = run_date)
        async def cancel_blacklist():
            user.blacklisted = False
            user.trigger_times = 0

        raise IgnoredException("reason")
