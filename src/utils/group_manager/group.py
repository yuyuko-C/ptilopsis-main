from random import choice

from src.utils.base.init_result import *

class Group:

    def __init__(self, group_id:int) -> None:
        self.group_id = group_id
        self.nickname = '未来永劫斩'
        self.members = None
        self.blacklisted = False
        self.send_message = True
        self.safe_group = False

    def acceptMessage(self):
        return not self.blacklisted

    def get_daily_rank(self):
        from src.utils.base.async_func import illusts
        nodes=[]
        for img in illusts['info']:
            sender=choice(self.members)
            info = []
            info.extend(['《{}》'.format(img['title']), 'Artist：'+str(img['user']['name'])])
            info.extend(['V / R：{} / {}'.format(img['total_view'], img['total_bookmarks'])])
            if (self.safe_group == True) or int(img['sanity_level']) < 4:
                info.append( str(image(abspath= img['file_path'])))
            else:
                info.append('[此图片限制级别过高，请自行访问P站查看]')
            info.append('ID:{}'.format(img['id']))
            nodes.append(node_make(sender['card'] or sender['nickname'], str(sender['user_id']), '\n'.join(info)))
        return forward(*nodes)

    def __str__(self):
        return '当前群名:{}\n接受推送:{}\n安全组:{}'.format(self.nickname,self.send_message,self.safe_group)