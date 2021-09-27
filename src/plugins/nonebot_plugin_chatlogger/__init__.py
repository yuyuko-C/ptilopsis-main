import os

from nonebot.plugin import require
from nonebot.adapters import Bot, Event
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.cqhttp import GroupIncreaseNoticeEvent,PrivateMessageEvent,GroupMessageEvent

from src.utils.base.event_center import EventCenter
from src.utils.logger_manager import Logger,LoggerManger,Chat_Topic
from src.utils.base.init_result import *
from src.utils.base.api import *
from src.config.path import *
from src.utils.base.log import logger

__plugin_name__='聊天记录器'




require_=require('nonebot_plugin_apsmatcher')
log_command:Matcher=require_.log_command
message_logger:Matcher=require_.message_logger



@log_command.handle()
async def deal_log_command(bot: Bot, event: GroupMessageEvent, state: T_State):
    logger.info('log command')
    event_msg=str(event.message).strip()
    msg_logger = LoggerManger.getLogger(event.group_id)

    if event_msg=='on':
        if msg_logger:
            await log_command.send(text('记录模块正在运转,授权人')+at(msg_logger.user_id))
        else:
            LoggerManger.createLogger(event.group_id, event.user_id)
            await log_command.send(text('指令正确，进入记录模式。\n白面鸮将记录在此之后的所有消息，直到授权人给出结束指令。授权人:')+at(event.user_id))
            await log_command.send('记录过程中，在消息最前方加上/，白面鸮就会忽略此消息。如果本次为误开启，请输入“取消”。')
            
    elif event_msg =='off':
        if msg_logger and msg_logger.state == 'logging':
            if (msg_logger.user_id==event.user_id) or (event.user_id in bot.config.superusers):
                ret = msg_logger.writeToMysql()
                if ret:
                    await log_command.send('记录已生成，请博士为本次记录取一个标题。')
                else:
                    await log_command.send('记录信息为空，本次记录已废弃。')
                    LoggerManger.deleteLogger(event.group_id)
        else:
            await log_command.send('白面鸮未处于记录状态，指令无效')
    
    elif event_msg =='list':
        log_path = LoggerManger.updateLogListImage(event.group_id)
        await log_command.send(image(abspath = log_path))

    elif event_msg =='help':
        await log_command.send(image(abspath=LOG_HELP_PATH))

    elif event_msg.startswith('see'):
        index = str(event.message).replace('see','').strip()
        if not index:
            await log_command.send("访问拒绝，未指定查看内容，请在命令后接上数字ID。")
        else:
            if not index.isdecimal():
                await log_command.send('访问拒绝，未获取到数字id，请重新输入。')
            else:
                index_list = LoggerManger.getVisiableTopic(event.group_id)
                index_list = [logger._model.id for logger in index_list ]
                if int(index) not in index_list:
                    await log_command.send("访问拒绝，请求的记录不存在，请重新输入。")
                else:
                    msg_logger = Logger(Chat_Topic.get_by_id(int(index)))
                    forward_message = msg_logger.getForwardMessage()

                    await EventCenter.notifyEvent('查看记录',bot=bot, event=event, state=state, matcher=log_command)
                    await log_command.send(f'查看记录：《{msg_logger.title}》')
                    await log_command.send('由于数据量较大，这将需要一定的时间，请稍等...')
                    await send_group_forward_msg(bot, event.group_id, forward_message)
    
    elif event_msg.startswith('drop'):
        if event.user_id in bot.config.superusers:
            index = str(event.message).replace('drop','').strip()
            if not index:
                await log_command.send("访问拒绝，未指定废弃内容，请在命令后接上数字ID。")
            else:
                if not index.isdecimal():
                    await log_command.send('访问拒绝，未获取到数字id，请重新输入。')
                else:
                    index_list = LoggerManger.getVisiableTopic(event.group_id)
                    index_list = [logger._model.id for logger in index_list ]
                    if int(index) not in index_list:
                        await log_command.send("访问拒绝，请求的记录不存在，请重新输入。")
                    else:
                        Chat_Topic.update(dropped=True).where(Chat_Topic.id == int(index))
                        await log_command.send('记录已废弃，感谢博士帮我擦拭身体，白面鸮感觉轻松了不少。')
        else:
            await log_command.send('身份信息校验失败，白面鸮拒绝为您提供服务。')
    
    

@message_logger.handle()
async def deal_log_message(bot: Bot, event: GroupMessageEvent, state: T_State):
    logger.info('log message')
    msg_logger = LoggerManger.getLogger(event.group_id)

    if msg_logger.state == 'logging':
        if (event.raw_message == '取消') and ((msg_logger.user_id == event.user_id) or (event.user_id in bot.config.superusers)):
            LoggerManger.deleteLogger(event.group_id)
            await message_logger.send('已退出记录模式，权限释放。')
        elif event.raw_message.startswith('/'):
            await message_logger.send(reply(event.message_id)+text('已忽略此条消息'))
        else:
            msg_logger.appendMessage(event)
    
    elif msg_logger.state == 'title':
        title = event.raw_message.strip()
        if (msg_logger.user_id == event.user_id) or (event.user_id in bot.config.superusers):
            if any([ ele in title for ele in ['CQ:','\n'] ]):
                await message_logger.send('检测到输入内容包含其他非法元素，请重新输入。')
            else:
                msg_logger.title = title
                await message_logger.send('是否要将此记录设为群私有？（Y/N）')

    elif msg_logger.state == 'permission':
        permission = event.raw_message.strip().lower()
        if (msg_logger.user_id == event.user_id) or (event.user_id in bot.config.superusers):
                if permission in ['y','yes']:
                    msg_logger.private = True
                elif permission in ['n','no']:
                    msg_logger.private = False
                else:
                    await message_logger.send('检测到输入内容包含其他非法元素，请重新输入。')
                    return
                
                await message_logger.send(f'记录完成，权限释放。感谢博士为此做出的努力。')                
                state['logger'] = msg_logger
                await EventCenter.notifyEvent('生成记录',bot=bot, event=event, state=state, matcher=message_logger)
                LoggerManger.deleteLogger(event.group_id)
    
    else:
        await message_logger.send('警告，记录状态发生未知错误。')
