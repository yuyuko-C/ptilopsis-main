from typing import *
from datetime import date,datetime,timedelta

from src.utils.logger_manager.model import Chat_Message,Chat_Topic
from src.utils.logger_manager.logger import Logger
from src.utils.base.text_to_img import text_to_img
from src.config.path import *


class LoggerManger:
    _register:Dict[int,Logger]={}

    @classmethod
    def hasPrivateTopic(cls, group_id:int):
        query = Chat_Topic.select().where(Chat_Topic.group_id == group_id, Chat_Topic.private== True)
        return bool(query)

    @classmethod
    def getVisiableTopic(cls, group_id:int = None):
        query =  Chat_Topic.select()
        for item in query:
            logger = Logger(item)
            # print(logger.is_visiable(group_id))
            if logger.is_visiable(group_id):
                yield logger

    @classmethod
    def getTopicList(cls, group_id:int = None):
        topics = cls.getVisiableTopic(group_id)
        wordList=[]
        [wordList.append(str(topic)) for topic in topics]
        return '\n\n'.join(wordList)

    @classmethod
    def updateLogListImage(cls, group_id:int):
        #更新记录列表的图片
        has_private = LoggerManger.hasPrivateTopic(group_id)
        if has_private:
            log_path = os.path.join(LOG_LIST_FOLDER_PATH, 'loglist_{}.jpg'.format(group_id))
        else:
            log_path = LOG_LIST_GENERAL_PATH
        text_to_img(cls.getTopicList(group_id), TEXTURE_PATH, log_path)
        return log_path

    @classmethod
    def getLogger(cls, group_id:int):
        if group_id in cls._register:
            return cls._register[group_id]

    @classmethod
    def createLogger(cls, group_id:int, user_id:int):
        if group_id not in cls._register:
            topic = Chat_Topic(log_date=date.today(),group_id=group_id ,user_id=user_id)
            logger = Logger(topic)
            cls._register[group_id] = logger
            return logger

    @classmethod
    def deleteLogger(cls, group_id:int):
        if group_id in cls._register:
            del cls._register[group_id]