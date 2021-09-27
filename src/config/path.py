import os


#一级文件夹

IMAGE_FOLDER_PATH=os.path.abspath("./src/data/image/")
VOICE_FOLDER_PATH=os.path.abspath("./src/data/voice/")
LOG_FOLDER_PATH=os.path.abspath("./src/data/log/")
LOG_LIST_FOLDER_PATH=os.path.abspath("./src/data/log_list/")

os.makedirs(IMAGE_FOLDER_PATH, exist_ok=True)
os.makedirs(VOICE_FOLDER_PATH, exist_ok=True)
os.makedirs(LOG_FOLDER_PATH, exist_ok=True)
os.makedirs(LOG_LIST_FOLDER_PATH, exist_ok=True)



#二级文件夹

DAILYRANK_FOLDER_PATH = os.path.join(IMAGE_FOLDER_PATH,'daily_rank')

os.makedirs(DAILYRANK_FOLDER_PATH, exist_ok=True)



#文件路径


TEXTURE_PATH = os.path.abspath("./src/config/TEXTURE.jpeg")
GROUPMANAGER_PATH = os.path.abspath("./src/config/GROUPs.r18")
USERMANAGER_PATH = os.path.abspath("./src/config/USERs.r18")

PTILOPSIS_PATH = os.path.join(IMAGE_FOLDER_PATH,'ptilopsis.jpg')
FEATHER_PATH = os.path.join(IMAGE_FOLDER_PATH,'feather.jpg')
POTENTIAL_PATH = os.path.join(IMAGE_FOLDER_PATH,'potential.jpg')
FUNCTION_PATH = os.path.join(IMAGE_FOLDER_PATH,'function.jpg')
LOG_HELP_PATH = os.path.join(IMAGE_FOLDER_PATH,'loghelp.jpg')
VERSION_PATH = os.path.join(IMAGE_FOLDER_PATH,'version.jpg')
LOG_LIST_GENERAL_PATH = os.path.join(LOG_LIST_FOLDER_PATH,'loglist_general.jpg')

ILLUSTION_PATH = os.path.join(DAILYRANK_FOLDER_PATH,'illustsinfo')



#代理

PROXY = 'http://127.0.0.1:10700'