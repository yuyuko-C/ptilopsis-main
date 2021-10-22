import logging

from nonebot import get_driver, export
from nonebot.log import logger, LoguruHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .config import Config

from src.utils.group_manager import GroupManager
from src.utils.user_manager import UserManager
from src.utils.logger_manager.model import Chat_Message
from src.utils.base.init_result import *
from src.utils.base.api import *
from src.utils.base.async_func import *

driver = get_driver()
global_config = driver.config
plugin_config = Config(**global_config.dict())

scheduler = AsyncIOScheduler()
export().scheduler = scheduler

__plugin_name__='定时任务'


async def _start_scheduler():
    if not scheduler.running:
        scheduler.configure(plugin_config.apscheduler_config)
        scheduler.start()
        logger.opt(colors=True).info("<y>Scheduler Started</y>")


if plugin_config.apscheduler_autostart:
    driver.on_startup(_start_scheduler)

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(plugin_config.apscheduler_log_level)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())



@scheduler.scheduled_job("cron",hour=4)
async def run_everyday_only_once():
    # 存储信赖与黑名单信息
    UserManager.save()
    # 存储群设置
    GroupManager.save()

    bot = get_bot()
    # 刷新群列表和群成员信息
    await loadInfo(bot)
    # 刷新P站榜单
    await dowanloadPixivRank(bot)
    # 重置完成公告
    for group_id in GroupManager._register:
        group = GroupManager.getGroup(group_id)
        if group.send_message:
            await send_group_msg(bot,group_id,'每日数据已刷新。输入/help了解白面鸮的使用方法。')

@scheduler.scheduled_job("cron",hour=12)
async def run_everyday_only_once(): 
    bot = get_bot()
    # 推送P站每日榜单
    for group_id in GroupManager._register:
        group = GroupManager.getGroup(group_id)
        if group.send_message:
            await send_group_msg(bot, group_id, '除了练习之外，每日看图也很重要。白面鸮已备好今天的资料')
            await send_group_msg(bot, group_id, '《Pixiv今日排行Top30》')
            await send_group_forward_msg(bot, group_id, group.get_daily_rank())

@scheduler.scheduled_job("cron",hour=13)
async def run_everyday_only_once(): 
    bot = get_bot()
    for user_id in UserManager._register:
        user_ins = UserManager.getUser(user_id)
        if user_ins.is_subscribed():
            group_id = user_ins.subs_group_id
            await send_private_msg(bot, user_id, group_id, text('别摸鱼了，博士。该午休了。'))

@scheduler.scheduled_job("interval",hours=4)
async def run_every_4_hour():
    #用于防止数据库断连
    LoggerManger.hasPrivateTopic(702754786)

@scheduler.scheduled_job("cron",hour='11,16-20/2')
async def run_every_2_hour():
    bot = get_bot()
    for user_id in UserManager._register:
        user_ins = UserManager.getUser(user_id)
        if user_ins.is_subscribed():
            group_id = user_ins.subs_group_id
            await send_private_msg(bot, user_id, group_id, text('博士，请注意劳逸结合。喝水、提肛、眼保健操，选一个执行吧~'))

@scheduler.scheduled_job("cron",hour=23)
async def run_everyday_only_once():
    bot = get_bot()
    for user_id in UserManager._register:
        user_ins = UserManager.getUser(user_id)
        if user_ins.is_subscribed():
            group_id = user_ins.subs_group_id
            await send_private_msg(bot, user_id, group_id, text('还不睡觉的屑博士~~~明天就会变成大笨蛋！'))