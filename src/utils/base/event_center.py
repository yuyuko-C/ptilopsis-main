from collections import defaultdict

class EventCenter:
    _event_dic=defaultdict(list)

    @classmethod
    def hasEvent(cls,event_name):
        return event_name in cls._event_dic.keys()

    @classmethod
    def addListener(cls,event_name,call_back):
        cls._event_dic[event_name].append(call_back)

    @classmethod
    async def notifyEvent(cls,event_name,**kargs):
        call_back_list=cls._event_dic[event_name]
        [await func(**kargs) for func in call_back_list]