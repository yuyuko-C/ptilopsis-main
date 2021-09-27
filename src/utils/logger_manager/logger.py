from datetime import datetime
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from src.utils.logger_manager.model import Chat_Message,Chat_Topic
from src.utils.group_manager import GroupManager
from src.utils.base.init_result import *

class Logger:

    def __init__(self,topic:Chat_Topic) -> None:
        self._model = topic
        self._log = []
        self.state = 'logging' # title

    def is_visiable(self, group_id:int):
        if self.dropped:
            return False
        else:
            if self.private and (group_id == None or self.group_id != group_id):
                return False
            else:
                return True

    def appendMessage(self, event:GroupMessageEvent):
        log={}
        log['send_time'] = datetime.now()
        log['message_id'] = event.message_id
        log['user_id'] = event.user_id
        log['plain_text'] = event.raw_message
        log['topic_id'] = self._model
        self._log.append(log)
    
    def writeToMysql(self):
        if self.state == 'logging':
            if self._log :
                self.save()
                Chat_Message.insert_many(self._log).execute()
                self.state = 'title'
                return True
            else:
                #如果记录消息条目为空，则废弃
                self.dropped = True
                return False
        else:
            print('记录已结束')

    def getForwardMessage(self):
        #导出次数+1
        Chat_Topic.update(out_times=Chat_Topic.out_times+1).where(Chat_Topic.id==self._model).execute()

        query = Chat_Message.select().join(Chat_Topic).where(Chat_Topic.id == self._model)
        nodes=[]
        for row in query:
            nodes.append(node_get(row.message_id))

        return forward(*nodes)

    def save(self):
        self._model.save()

    def __str__(self) -> str:
        index = self._model.id
        title = self.title
        group_id = self.group_id
        date_ = self._model.log_date
        nickname = GroupManager.getGroup(group_id).nickname
        return f'{index}.《{title}》\n来自群：{nickname}\n日期：{date_}'

    @property
    def title(self):
        return self._model.title

    @title.setter
    def title(self, value:str):
        self._model.title = value
        self.state = 'permission'
        self.save()

    @property
    def user_id(self):
        return int(self._model.user_id)

    @user_id.setter
    def user_id(self, value:str):
        self._model.user_id = value
        self.save()

    @property
    def group_id(self):
        return int(self._model.group_id)

    @group_id.setter
    def group_id(self, value:str):
        self._model.group_id = value
        self.save()

    @property
    def private(self):
        return self._model.private

    @private.setter
    def private(self, value:str):
        self._model.private = value
        self.save()

    @property
    def dropped(self):
        return self._model.dropped

    @dropped.setter
    def dropped(self, value:bool):
        self._model.dropped = value
        self.save()
