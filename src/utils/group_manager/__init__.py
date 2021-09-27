from typing import *
import pickle

from src.utils.group_manager.group import Group
from src.config.path import *

class GroupManager:
    _register:Dict[int,Group] = {}
    
    @classmethod
    def load(cls):
        if os.path.exists(USERMANAGER_PATH):
            with open(GROUPMANAGER_PATH,'rb') as f:
                cls._register:Dict[int,Group] = pickle.load(f)

    @classmethod
    def save(cls):
        with open(GROUPMANAGER_PATH,'wb') as f:
            pickle.dump(cls._register, f)
    
    @classmethod
    def hasGroup(cls,group_id:int):
        return group_id in cls._register.keys()

    @classmethod
    def deleteGroup(cls,group_id:int):
        del cls._register[group_id]

    @classmethod
    def getGroup(cls,group_id:int)->Group:
        if not cls.hasGroup(group_id):
            group_ins = Group(group_id)
            cls._register[group_id]=group_ins
        return cls._register[group_id]
