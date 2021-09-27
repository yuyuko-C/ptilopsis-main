from typing import *
import pickle

from src.utils.user_manager.user import User
from src.config.path import *

class UserManager:
    _register:Dict[int,User] = {}
    
    @classmethod
    def load(cls):
        if os.path.exists(USERMANAGER_PATH):
            with open(USERMANAGER_PATH,'rb') as f:
                cls._register:Dict[int,User] = pickle.load(f)

    @classmethod
    def save(cls):
        with open(USERMANAGER_PATH,'wb') as f:
            users=cls._register.values()
            for user_ins in users:
                user_ins.trigger_times = 0
                user_ins.blacklisted = False
            pickle.dump(cls._register, f)

    @classmethod
    def hasUser(cls,user_id:int):
        return user_id in cls._register.keys()

    @classmethod
    def deleteUser(cls,user_id:int):
        del cls._register[user_id]

    @classmethod
    def getUser(cls,user_id:int)->User:
        if not cls.hasUser(user_id):
            user_ins=User(user_id)
            cls._register[user_id]=user_ins
        return cls._register[user_id]

    @classmethod
    def blacklistUser(cls, user_id:int):
        cls.getUser(user_id).blacklisted = True
        cls.unsubs_greeting(user_id)