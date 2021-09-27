import os
import json
from typing import Union

from nonebot.adapters.cqhttp.message import Message, MessageSegment

from src.config.path import IMAGE_FOLDER_PATH, VOICE_FOLDER_PATH
from src.utils.base.log import logger as log



def image(img_name: str = None, path: str = '', abspath: str = None, b64: str = None):
    if abspath:
        if os.path.exists(abspath):
            return MessageSegment.image("file:///" + abspath)
        else:
            return ''
    elif b64:
        if b64.find('base64://') != -1:
            return MessageSegment.image(b64)
        else:
            return MessageSegment.image('base64://' + b64)
    else:
        img_name = str(img_name)
        if img_name.find('http') == -1:
            if len(img_name.split('.')) == 1:
                img_name += '.jpg'
            file_path=os.path.join(IMAGE_FOLDER_PATH,path,img_name)
            if os.path.exists(file_path):
                return MessageSegment.image("file:///" + file_path)
            else:
                log.warning(f"图片 {path}/{img_name}缺失.")
                return ''
        else:
            return MessageSegment.image(img_name)


def at(qq):
    return MessageSegment.at(qq)


def record(voice_name='', path=''):
    if len(voice_name.split('.')) == 1:
        voice_name += '.mp3'
    if path == "":
        name = VOICE_FOLDER_PATH + "{}.".format(voice_name)
    else:
        name = VOICE_FOLDER_PATH + "{}/{}".format(path, voice_name)
    if voice_name.find('http') == -1:
        if os.path.exists(name):
            result = MessageSegment.record("file:///" + name)
            return result
        else:
            log.warning(f"语音{path}/{voice_name}缺失...")
            return ""
    else:
        return MessageSegment.record(voice_name)


def text(msg):
    return MessageSegment.text(msg)


def reply(msg_id):
    return MessageSegment.reply(msg_id)


def contact_user(qq):
    return MessageSegment.contact_user(qq)


def share(url, title, content='', image_url=''):
    return MessageSegment.share(url, title, content, image_url)


def _xml(data):
    return MessageSegment.xml(data)


def _json(data):
    data = json.dumps(data)
    return MessageSegment.json(data)


def face(id_):
    return MessageSegment.face(id_)


def poke(qq):
    return MessageSegment('poke', {"qq": qq})

def node_make(senderName:str,senderId:str,content:str):
    return {
        "type": "node",
        "data": {
            "name": senderName,
            "uin": senderId,
            "content": content
        }
    }


def node_get(messageId:str):
    return {
        "type": "node",
        "data": {
            "id": messageId
        }
    }


def forward(*nodeargs): 
    f=[]
    for node in nodeargs:
        if node['type']=='node':
            f.append(node)
        else:
            raise TypeError('forward element must be node')
    return f

# if __name__ == '__main__':
#     print(get_record_result("dadada", "", type="amr"))
