from nonebot import on_command,on_message,on_notice,on_request,on_keyword,on_regex
from nonebot.adapters.cqhttp.event import MessageEvent, PokeNotifyEvent, PrivateMessageEvent
from nonebot.matcher import Matcher
from nonebot.plugin import export,require
from nonebot.rule import to_me,Rule
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.message import run_postprocessor,run_preprocessor

from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import GroupRequestEvent,GroupMessageEvent,FriendRequestEvent
from nonebot.adapters.cqhttp.permission import *


from src.utils.logger_manager import LoggerManger
from src.utils.group_manager import GroupManager
from src.utils.user_manager import UserManager
from src.config import path, doc, __version__
from src.utils.base.event_center import EventCenter
from src.utils.base.init_result import *
from src.utils.base.api import *
from src.utils.base.text_to_img import text_to_img
from src.utils.base.async_func import *
from src.utils.base.log import logger as log



import nonebot


__plugin_name__='事件触发器中心'


global_config = nonebot.get_driver().config

superusers=list(global_config.superusers)
nickname=list(global_config.nickname)

require_=require('nonebot_plugin_apscheduler')
scheduler=require_.scheduler

export_=export()


driver = nonebot.get_driver()



# nonebot2 Hook函数

@driver.on_startup
async def start():
    #1.开启事件监听
    EventCenter.addListener('获得灰羽',getFeatherCallback)
    EventCenter.addListener('生成记录',logCreateCallback)
    EventCenter.addListener('查看记录',logSeeCallback)
    EventCenter.addListener('触发插件',triggerPlugin)
    
    #2.读取保存的信息
    UserManager.load()
    GroupManager.load()
    
    #3.生成图片
    text_to_img(doc.FUNCTION_HELP, path.TEXTURE_PATH, path.FUNCTION_PATH)
    text_to_img(doc.PTILOPSIS, path.TEXTURE_PATH, path.PTILOPSIS_PATH)
    text_to_img(doc.POTENTIAL, path.TEXTURE_PATH, path.POTENTIAL_PATH)
    text_to_img(doc.GRAY_FEATHER, path.TEXTURE_PATH, path.FEATHER_PATH)
    text_to_img(doc.LOG_HELP, path.TEXTURE_PATH, path.LOG_HELP_PATH)
    #版本
    with open('./src/data/version/{}.log'.format(__version__),'r',encoding='utf8') as f:
        text_to_img(f.read(), path.TEXTURE_PATH, path.VERSION_PATH)
    #记录列表
    for group_id in GroupManager._register:
        LoggerManger.updateLogListImage(group_id)
    log.info('图片初始化完毕')

    # 读取本地的pixiv排行信息
    if os.path.exists(path.ILLUSTION_PATH):
        with open(path.ILLUSTION_PATH,'r') as f:
            illusts['info'] = json.load(f)['info']

@driver.on_bot_connect
async def initial_data(bot: Bot):
    bot.config.api_timeout=120


    #1.初始化群信息
    await loadInfo(bot)
    log.info('群信息初始化完毕')

    # #2下载每日排行榜图片
    # await dowanloadPixivRank(bot)

    #3.清除多余的图片缓存
    await clean_image_file()

    log.info('初始化完成')

@driver.on_shutdown
async def save_data():
    # 存储信赖与黑名单信息
    UserManager.save()
    # 存储群设置
    GroupManager.save()
    # 清除多余的图片缓存
    await clean_image_file()
    print('关闭机器人')

@run_preprocessor
async def check_trigger_rate(matcher: Matcher, bot: Bot, event: Event, state: T_State):
    if isinstance(event,PokeNotifyEvent):
        pass
    elif isinstance(event,GroupMessageEvent):
        if LoggerManger.getLogger(event.group_id):
            if not event.raw_message.startswith('/'):
                pass
        else:
            state['scheduler']=scheduler
            await EventCenter.notifyEvent('触发插件',bot=bot, event=event, state=state, matcher=matcher)



###### 函数定义 ######


def acceptMessage() -> Rule:
    """
    :说明:

      匹配接受的群消息

    :参数:

      无
    """

    async def _accept_message(bot: "Bot", event: "Event", state: T_State) -> bool:
        if isinstance(event,(PokeNotifyEvent,GroupMessageEvent)):
            group_access= GroupManager.getGroup(event.group_id).acceptMessage()
            member_access=UserManager.getUser(event.user_id).acceptMessage()
            return group_access and member_access
        else:
            return False

    return Rule(_accept_message)


def loggingGroup() -> Rule:
    """
    :说明:

      匹配正在记录讨论的群消息

    :参数:

      "group_id" ：群ID
    """

    async def _is_logging(bot: "Bot", event: "Event", state: T_State) -> bool:
        if isinstance(event,GroupMessageEvent):
            return bool(LoggerManger.getLogger(event.group_id))

    return Rule(_is_logging)



###### on_command ######
set_matcher=on_command('set', permission=SUPERUSER, priority=1)
export_.set_command=set_matcher
@set_matcher.handle()
async def setting(bot: Bot, event: MessageEvent, state: T_State):
    # 句式 /set user/group id property Or /set @user_id property
    if len(event.message) == 1:
        messages = event.message.extract_plain_text().strip()
        obj, id_, property_ = messages.split(' ')

    elif len(event.message) == 2:
        obj = 'user'
        id_ =  event.message[0].data['qq']
        property_ = event.message[1].strip()

    else:
        await set_matcher.finish('格式错误。句式 /set user/group id property Or /set @user_id property')

    obj_list = ('user','group')
    if obj not in obj_list:
        await set_matcher.finish('设置格式错误。obj只能是{}'.format('/'.join(obj_list)))

    propery_list = ('enable','ban','open','close','safe','unsafe')
    if property_ not in propery_list:
        await set_matcher.finish('设置格式错误。property只能是{}'.format('/'.join(propery_list)))


    async def set_user(user_id:int, enable:str):
        if not UserManager.hasUser(user_id):
            await set_matcher.finish('不存在此用户')

        if enable=='enable':
            UserManager.getUser(user_id).blacklisted=False
        elif enable=='ban':
            UserManager.blacklistUser(user_id)
        else:
            await set_matcher.finish('user无此设置选项。')

    async def set_group(group_id:int, enable:str):
        if not GroupManager.hasGroup(group_id):
            await set_matcher.finish('不存在此群')

        if enable=='enable':
            GroupManager.getGroup(group_id).blacklisted=False
        elif enable=='ban':
            GroupManager.getGroup(group_id).blacklisted=True
        elif enable=='open':
            GroupManager.getGroup(group_id).send_message=True 
        elif enable=='close':
            GroupManager.getGroup(group_id).send_message=False
        elif enable=='safe':
            GroupManager.getGroup(group_id).safe_group=True
        elif enable=='unsafe':
            GroupManager.getGroup(group_id).safe_group=False  
        else:
            await set_matcher.finish('group无此设置选项。')


    if obj == 'user':
        await set_user(int(id_),property_)
    elif obj == 'group':
        await set_group(int(id_),property_)

    await set_matcher.finish('设置成功')


#只处理有关聊天记录器命令
log_matcher= on_command('log',rule=acceptMessage(),permission=GROUP,priority=1,block=True)
export_.log_command=log_matcher


#只处理有关搜图命令
pic_matcher= on_command('spi',aliases={"spt","spa"},rule=acceptMessage(),permission=GROUP,priority=1,block=True)
export_.pic_command=pic_matcher


#只处理有关搜图命令
info_matcher= on_command('info',rule=acceptMessage(),permission=GROUP,priority=1,block=True)
export_.info_command=info_matcher
@info_matcher.handle()
async def subs_command(bot: Bot, event: GroupMessageEvent, state: T_State):
    user = UserManager.getUser(event.user_id)
    group = GroupManager.getGroup(event.group_id)
    await info_matcher.finish(text(str(user)+'\n\n'+str(group)))


#只处理有关订阅命令
subs_matcher= on_command('subs',rule=acceptMessage(),permission=GROUP,priority=1,block=True)
export_.subs_command=subs_matcher
@subs_matcher.handle()
async def subs_command(bot: Bot, event: GroupMessageEvent, state: T_State):
    msg=event.raw_message.replace('/subs','').strip()
    user_ins =  UserManager.getUser(event.user_id)

    if msg == 'on':
        res = user_ins.apply_subscribe(event.group_id)
        if res:
            await subs_matcher.finish(reply(event.message_id)+text('往后就由白面鸮照顾您的身体健康啦，请多多指教！'))
        else:
            await subs_matcher.finish(reply(event.message_id)+text('博士正在白面鸮的关怀之下哦~'))

    elif msg == 'off':
        res = user_ins.remove_subscribe()
        if res:
            await subs_matcher.finish(reply(event.message_id)+text('很抱歉打扰到了博士，白面鸮不会再来了...'))
        else:
            await subs_matcher.finish(reply(event.message_id)+text('经查询博士并不在白面鸮的服务对象之中，博士就这么讨厌我吗？'))


#低一个优先级，让所有命令检查都不符之后再处理这里
#用于介绍设定和指引帮助的命令
other_matcher= on_command('',rule=acceptMessage(),permission=GROUP,priority=2,block=True)
export_.other_command=other_matcher
@other_matcher.handle()
async def other_command(bot: Bot, event: GroupMessageEvent, state: T_State):
    print('触发其他系列命令')
    msg=event.raw_message.strip('/')
    if msg == '白面鸮':
        await other_matcher.finish(image(abspath= path.PTILOPSIS_PATH))
    elif msg == '灰羽':
        await other_matcher.finish(image(abspath= path.FEATHER_PATH))
    elif msg == '潜能':
        await other_matcher.finish(image(abspath= path.POTENTIAL_PATH))
    elif msg == 'help':
        await other_matcher.finish(image(abspath= path.FUNCTION_PATH))
    elif msg == 'version':
        await other_matcher.finish(image(abspath= path.VERSION_PATH))
    elif msg == '更新日榜':
        await dowanloadPixivRank(bot)
    elif msg == '发送日榜':
        group = GroupManager.getGroup(event.group_id)
        await send_group_forward_msg(bot, event.group_id, group.get_daily_rank())
    elif msg == '发送日榜全部':
        # 推送P站每日榜单
        for group_id in GroupManager._register:
            group = GroupManager.getGroup(group_id)
            if group.send_message:
                await send_group_msg(bot, group_id, '除了练习之外，每日看图也很重要。白面鸮已备好今天的资料')
                await send_group_msg(bot, group_id, '《Pixiv今日排行Top30》')
                await send_group_forward_msg(bot, group_id, group.get_daily_rank())
        pass
    elif msg == '保存':
        # 存储信赖与黑名单信息
        UserManager.save()
        # 存储群设置
        GroupManager.save()
        # 清除多余的图片缓存
        await clean_image_file()
        await other_matcher.finish('保存结束')
    else:
        if LoggerManger.getLogger(event.group_id):
            await other_matcher.finish('收到忽略指令，信息忽略已完成。')
        else:
            await other_matcher.finish('指令错误。输入/help可以更加了解白面鸮。')




###### on_message ######

#处理申请记录的群的信息
message_matcher=on_message(rule=loggingGroup(),permission=GROUP,priority=4,block=False)
export_.message_logger=message_matcher




###### on_request ######

approve = on_request(priority=1)

@approve.handle()
async def auto_approve(bot: Bot, event: Event, state: T_State):
    if isinstance(event,GroupRequestEvent):
        if event.sub_type == 'invite':
            try:
                await set_group_add_request(bot, event.flag, event.sub_type, True)
            except ActionFailed as e:
                pass
            finally:
                await loadInfo(bot)
                await send_group_msg(bot, event.group_id, '前莱茵生命数据维护员白面鸮，输入/help可了解白面鸮的使用方法。')
                await send_private_msg(bot, 1061439585, None, '已同意进群：{}'.format(event.group_id))
        
    elif isinstance(event,FriendRequestEvent):
        await set_friend_add_request(bot, event.flag, True)
        await send_private_msg(bot, 1061439585, None, '已同意添加好友：{}'.format(event.user_id))



###### on_notice ######

notice = on_notice(rule=acceptMessage()&to_me(),priority=1)
@notice.handle()
async def accept_group_poke(bot: Bot, event: Event, state: T_State):
    if isinstance(event, PokeNotifyEvent):
        if random.random() < 0.1 :
            state['value'] = 2
            await EventCenter.notifyEvent('获得灰羽',bot=bot, event=event, state=state, matcher=notice)
        else:
            await notice.send(text(random.choice(doc.LINES_GENERAL)))
    pass