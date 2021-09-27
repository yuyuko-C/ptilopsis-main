class Package:

    def __init__(self) -> None:
        self._container = {}

    def pushItem(self, itemName:str, count:int = 1):
        self._container[itemName] += count

    def popItem(self, itemName:str, count:int = 1):
        if self.hasItem(itemName):
            if self._container[itemName] >= count:
                self._container[itemName] -= count
                return True
        return False

    def getItemNum(self, itemName:str):
        if self.hasItem(itemName):
            return self._container[itemName]
        else:
            return 0
    
    def hasItem(self, itemName:str):
        return itemName in self._container
        

class Potential:
    '''
    潜能仅仅影响白面鸮的反应与剧情进度，不对插件使用次数做任何限制
    与之相对的需要做恶意触发检测
    '''
    level_req = [0,100,200,400,800,1600]

    @classmethod
    def getLevel(cls, value:int):
        for i in range(len(cls.level_req)):
            if value < cls.level_req[i]:
                return i
        return 5

    @classmethod
    def getInfo(cls, value:int):
        trust_level = cls.getLevel(value)
        return f'潜能等级:{trust_level}    灰羽：({value}/{cls.level_req[trust_level]})'

