
from peewee import *
from src.utils.base.model_func import Base_Model




class Chat_Topic(Base_Model):
    log_date=DateField()
    group_id=CharField()
    user_id=CharField()
    title=CharField()
    dropped=BooleanField()
    private=BooleanField()
    out_times=IntegerField()


class Chat_Message(Base_Model):
    send_time=DateTimeField()
    user_id=CharField()
    message_id=CharField()
    plain_text=TextField()
    topic=ForeignKeyField(Chat_Topic,backref='msgs')

# Chat_Message.drop()
# Chat_Topic.drop()

Chat_Topic.instance()
Chat_Message.instance()

Chat_Topic.reset_auto_increment()
Chat_Message.reset_auto_increment()

