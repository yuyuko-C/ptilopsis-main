from src.utils.base.tools import Package,Potential


class User:
    
    def __init__(self, user_id:int) -> None:
        self.user_id = user_id
        self.nick_name = '失去姓名的小柯基'
        self.feathers = 0
        self.trigger_times = 0
        self.package = Package()
        
        self.subs_group_id = None
        self.blacklisted = False

    def acceptMessage(self):
        return not self.blacklisted

    def getPotentialLevel(self):
        return Potential.getLevel(self.feathers)

    def getTrustInfo(self):
        return Potential.getInfo(self.feathers)

    def getItem(self, itemName:str, count:int = 1):
        self.package.pushItem(itemName, count)

    def useItem(self, itemName:str, count:int = 1):
        if self.package.getItemNum(itemName) >= count:
            self.package.popItem(itemName, count)

    def is_subscribed(self):
        return self.subs_group_id != None

    def apply_subscribe(self, group_id:int):
        if self.is_subscribed():
            return False
        else:
            self.subs_group_id = group_id
            return True

    def remove_subscribe(self):
        if self.is_subscribed():
            self.subs_group_id = None
            return True
        else:
            return False

    def __str__(self) -> str:
        info=f'Dr.{self.nick_name}\n根据您与白面鸮的来往记录，查询到的信息如下：\n'
        info += self.getTrustInfo() + '\n'
        info += '触发频率:{}/分钟\n黑名单之中:{}'.format(self.trigger_times,self.blacklisted)
        return info
