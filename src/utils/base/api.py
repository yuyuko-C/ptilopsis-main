from typing import Coroutine, Union
from pixivpy_async.retry import retry

import nonebot

from nonebot.adapters.cqhttp.bot import *
from nonebot.adapters.cqhttp.message import *
from nonebot.adapters.cqhttp.exception import *

def get_bot():
    return nonebot.get_bots()["2648250775"]

retryable_error = (NetworkError,)

@retry(*retryable_error)
def send_private_msg(bot:Bot, user_id:int, group_id:int, message:Message, auto_escape:bool = False)->Coroutine:
    """[发送私聊消息]

    Args:
        bot (Bot): [description]
        user_id (int): [对方 QQ 号]
        group_id (int): [主动发起临时会话群号]
        message (Message): [要发送的内容]
        auto_escape (bool, optional): [消息内容是否作为纯文本发送 ( 即不解析 CQ 码 ) , 只在 message 字段是字符串时有效]. Defaults to False.
    
    Returns:
        Coroutine: [description]
    """
    return bot.call_api('send_private_msg',user_id = user_id, group_id = group_id, message = message, auto_escape = auto_escape)

@retry(*retryable_error)
def send_group_msg(bot:Bot, group_id:int, message:Message, auto_escape:bool = False)->Coroutine:
    """[发送群消息s]

    Args:
        bot (Bot): [群号]
        group_id (int): [要发送的内容]
        message (Message): [description]
        auto_escape (bool, optional): [消息内容是否作为纯文本发送 ( 即不解析 CQ 码) , 只在 message 字段是字符串时有效]. Defaults to False.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('send_group_msg', group_id = group_id, message = message, auto_escape = auto_escape)

@retry(*retryable_error)
def send_group_forward_msg(bot:Bot, group_id:int, messages:Message)->Coroutine:
    """[发送合并转发 ( 群 )]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        messages (Message): [自定义转发消息, 具体看 CQcode]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('send_group_forward_msg', group_id = group_id, messages = messages)

@retry(*retryable_error)
def delete_msg(bot:Bot, message_id:int)->Coroutine:
    """[撤回消息]

    Args:
        bot (Bot): [description]
        message_id (int): [消息 ID]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('delete_msg',message_id = message_id)

@retry(*retryable_error)
def get_msg(bot:Bot, message_id:int)->Coroutine:
    """[获取消息]

    Args:
        bot (Bot): [description]
        message_id (int): [消息id]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_msg',message_id = message_id)

@retry(*retryable_error)
def get_forward_msg(bot:Bot, message_id:int)->Coroutine:
    """获取合并转发内容

    Args:
        bot (Bot): [description]
        message_id (int): [消息id]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_forward_msg',message_id = message_id)

@retry(*retryable_error)
def get_image(bot:Bot, file:str)->Coroutine:
    """[获取图片信息]

    Args:
        bot (Bot): [description]
        file (str): [图片缓存文件名]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_image',file = file)

@retry(*retryable_error)
def set_group_kick(bot:Bot, user_id:int, group_id:int, reject_add_request:bool = False)->Coroutine:
    """[群组踢人]

    Args:
        bot (Bot): [description]
        user_id (int): [要踢的 QQ 号]
        group_id (int): [群号]
        reject_add_request (bool, optional): [拒绝此人的加群请求]. Defaults to False.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_kick',user_id = user_id, group_id = group_id, reject_add_request = reject_add_request)

@retry(*retryable_error)
def set_group_ban(bot:Bot, user_id:int, group_id:int, duration:int = 30 * 60)->Coroutine:
    """[群组单人禁言]

    Args:
        bot (Bot): [description]
        user_id (int): [要禁言的 QQ 号]
        group_id (int): [群号]
        duration (int, optional): [禁言时长, 单位秒, 0 表示取消禁言]. Defaults to 30*60.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_ban',user_id = user_id, group_id = group_id, duration = duration)

@retry(*retryable_error)
def set_group_anonymous_ban(bot:Bot, group_id:int, flag:str, duration:int = 30 * 60)->Coroutine:
    """[群组匿名用户禁言]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        flag (str): [要禁言的匿名用户的 flag（需从群消息上报的数据中获得）]
        duration (int, optional): [禁言时长, 单位秒, 无法取消匿名用户禁言]. Defaults to 30*60.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_anonymous_ban',group_id = group_id, flag = flag, duration = duration)

@retry(*retryable_error)
def set_group_whole_ban(bot:Bot, group_id:int, enable:bool = True)->Coroutine:
    """[群组全员禁言]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        enable (bool): [是否禁言]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_anonymous_ban',group_id = group_id, enable = enable)

@retry(*retryable_error)
def set_group_admin(bot:Bot, user_id:int, group_id:int, enable:bool = True)->Coroutine:
    """[群组设置管理员]

    Args:
        bot (Bot): [description]
        user_id (int): [要设置管理员的 QQ 号]
        group_id (int): [群号]
        enable (bool, optional): [true 为设置, false 为取消]. Defaults to True.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_admin',user_id = user_id, group_id = group_id, enable = enable)

@retry(*retryable_error)
def set_group_card(bot:Bot, user_id:int, group_id:int, card:str = '')->Coroutine:
    """[设置群名片 ( 群备注 )]

    Args:
        bot (Bot): [description]
        user_id (int): [要设置的 QQ 号]
        group_id (int): [群号]
        card (str, optional): [群名片内容, 不填或空字符串表示删除群名片]. Defaults to ''.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_card',user_id = user_id, group_id = group_id, card = card)

@retry(*retryable_error)
def set_group_name(bot:Bot, group_id:int, group_name:str)->Coroutine:
    """[summary]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        group_name (str): [新群名]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_name', group_id = group_id, group_name = group_name)

@retry(*retryable_error)
def set_group_leave(bot:Bot, group_id:int, is_dismiss:bool = False)->Coroutine:
    """[退出群组]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        is_dismiss (bool): [是否解散, 如果登录号是群主, 则仅在此项为 true 时能够解散]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_leave', group_id = group_id, is_dismiss = is_dismiss)

@retry(*retryable_error)
def set_group_special_title(bot:Bot, user_id:int, group_id:int, special_title:str = '', duration:int = -1)->Coroutine:
    """[设置群组专属头衔]

    Args:
        bot (Bot): [description]
        user_id (int): [要设置的 QQ 号]
        group_id (int): [群号]
        special_title (str, optional): [专属头衔, 不填或空字符串表示删除专属头衔]. Defaults to None.
        duration (int, optional): [专属头衔有效期, 单位秒, -1 表示永久, 不过此项似乎没有效果, 可能是只有某些特殊的时间长度有效, 有待测试]. Defaults to -1.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_special_title',user_id = user_id, group_id = group_id, special_title = special_title, duration = duration)

@retry(*retryable_error)
def set_friend_add_request(bot:Bot, flag:str, approve:bool = True, remark:str = '')->Coroutine:
    """[处理加好友请求]

    Args:
        bot (Bot): [description]
        flag (str): [加好友请求的 flag（需从上报的数据中获得）]
        approve (bool): [是否同意请求]
        remark (str, optional): [添加后的好友备注（仅在同意时有效）]. Defaults to ''.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_friend_add_request',flag = flag, approve = approve, remark = remark)

@retry(*retryable_error)
def set_group_add_request(bot:Bot, flag:str, sub_type:str, approve:bool = True, reason:str = '')->Coroutine:
    """[处理加群请求／邀请]

    Args:
        bot (Bot): [description]
        flag (str): [加群请求的 flag（需从上报的数据中获得）]
        sub_type (str): [add 或 invite, 请求类型（需要和上报消息中的 sub_type 字段相符）]
        approve (bool, optional): [是否同意请求／邀请]. Defaults to True.
        reason (str, optional): [拒绝理由（仅在拒绝时有效）]. Defaults to ''.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_add_request',flag = flag, sub_type = sub_type, approve = approve, reason = reason)

@retry(*retryable_error)
def get_stranger_info(bot:Bot, user_id:int, no_cache:bool = False)->Coroutine:
    """[获取陌生人信息]

    Args:
        bot (Bot): [description]
        user_id (int): [QQ 号]
        no_cache (bool, optional): [是否不使用缓存（使用缓存可能更新不及时, 但响应更快）]. Defaults to False.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_group_add_request',user_id = user_id, no_cache = no_cache)

@retry(*retryable_error)
def get_friend_list(bot:Bot)->Coroutine:
    """[获取好友列表]

    Args:
        bot (Bot): [description]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_friend_list')

@retry(*retryable_error)
def delete_friendt(bot:Bot, friend_id:int)->Coroutine:
    """[删除好友]

    Args:
        bot (Bot): [description]
        friend_id (int): [好友 QQ 号]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('delete_friendt', friend_id = friend_id)

@retry(*retryable_error)
def get_group_info(bot:Bot, group_id:int, no_cache:bool = False)->Coroutine:
    """[获取群信息]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        no_cache (bool, optional): [是否不使用缓存（使用缓存可能更新不及时, 但响应更快）]. Defaults to False.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_info', group_id = group_id, no_cache = no_cache)

@retry(*retryable_error)
def get_group_list(bot:Bot)->Coroutine:
    """[获取群列表]

    Args:
        bot (Bot): [description]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_list')

@retry(*retryable_error)
def get_group_member_info(bot:Bot, user_id:int, group_id:int, no_cache:bool = False)->Coroutine:
    """[获取群成员信息]

    Args:
        bot (Bot): [description]
        user_id (int): [QQ 号]
        group_id (int): [群号]
        no_cache (bool, optional): [是否不使用缓存（使用缓存可能更新不及时, 但响应更快）]. Defaults to False.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_member_info',user_id = user_id, group_id = group_id, no_cache = no_cache)

@retry(*retryable_error)
def get_group_member_list(bot:Bot, group_id:int)->Coroutine:
    """[获取群成员列表]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_member_list', group_id = group_id)

@retry(*retryable_error)
def get_group_honor_info(bot:Bot, group_id:int, type:bool = False)->Coroutine:
    """[获取群荣誉信息]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        type (bool, optional): [要获取的群荣誉类型, 可传入 talkative performer legend strong_newbie emotion 以分别获取单个类型的群荣誉数据, 或传入 all 获取所有数据]. Defaults to False.

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_honor_info', group_id = group_id, type = type)

@retry(*retryable_error)
def set_restart(bot:Bot, delay:int = 0)->Coroutine:
    """[重启 go-cqhttp]

    Args:
        bot (Bot): [description]
        delay (int): [要延迟的毫秒数, 如果默认情况下无法重启, 可以尝试设置延迟为 2000 左右]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('set_restart', delay = delay)

@retry(*retryable_error)
def get_group_system_msg(bot:Bot)->Coroutine:
    """[获取群系统消息]

    Args:
        bot (Bot): [description]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_system_msg')

@retry(*retryable_error)
def upload_group_file(bot:Bot, group_id:int, file:str, name:str, folder:str)->Coroutine:
    """[上传群文件.在不提供 folder 参数的情况下默认上传到根目录]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        file (str): [本地文件路径]
        name (str): [储存名称]
        folder (str): [父目录ID]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('upload_group_file', group_id = group_id, file = file, name = name, folder = folder)

@retry(*retryable_error)
def get_group_file_system_info(bot:Bot, group_id:int)->Coroutine:
    """[获取群文件系统信息]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_file_system_info', group_id = group_id)

@retry(*retryable_error)
def get_group_root_files(bot:Bot, group_id:int)->Coroutine:
    """[获取群根目录文件列表]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_root_files', group_id = group_id)

@retry(*retryable_error)
def get_group_files_by_folder(bot:Bot, group_id:int, folder_id:int)->Coroutine:
    """[获取群子目录文件列表]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        folder_id (int): [文件夹ID 参考 Folder 对象]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_files_by_folder', group_id = group_id, folder_id = folder_id)

@retry(*retryable_error)
def get_group_file_url(bot:Bot, group_id:int, busid:int)->Coroutine:
    """[获取群文件资源链接]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        folder_id (int): [文件ID 参考 File 对象]
        busid (int): [文件类型 参考 File 对象]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_group_file_url', group_id = group_id, busid = busid)

@retry(*retryable_error)
def get_status(bot:Bot)->Coroutine:
    """[获取状态]

    Args:
        bot (Bot): [description]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_status')

@retry(*retryable_error)
def download_file(bot:Bot, url:str, thread_count:int, headers:Union[str,list])->Coroutine:
    """[下载文件到缓存目录]

    Args:
        bot (Bot): [description]
        url (str): [链接地址]
        thread_count (int): [下载线程数]
        headers (Union[str,list]): [自定义请求头]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_status', url = url, thread_count = thread_count, headers = headers)

@retry(*retryable_error)
def get_group_msg_history(bot:Bot, group_id:int, message_seq:int)->Coroutine:
    """[获取群消息历史记录]

    Args:
        bot (Bot): [description]
        group_id (int): [群号]
        message_seq (int): [起始消息序号, 可通过 get_msg 获得]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_status', message_seq = message_seq, group_id = group_id)

@retry(*retryable_error)
def check_url_safely(bot:Bot, url:str)->Coroutine:
    """[检查链接安全性]

    Args:
        bot (Bot): [description]
        url (str): [需要检查的链接]

    Returns:
        Coroutine: [description]
    """
    return bot.call_api('get_status', url = url)

