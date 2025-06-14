# 卡牌类型
CARD_TYPES = ['attack', 'defense', 'curse', 'heal']

# 卡牌数值范围
CARD_VALUES = list(range(1, 17))  # 1-16

# 屏幕基准分辨率（原设计）
BASE_WIDTH = 1200
BASE_HEIGHT = 800
# 目标分辨率
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
# 缩放系数
SCALE_X = SCREEN_WIDTH / BASE_WIDTH
SCALE_Y = SCREEN_HEIGHT / BASE_HEIGHT
SCALE = min(SCALE_X, SCALE_Y)

#屏幕大小（兼容旧变量名）
screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT

#卡牌图片
attack_card="assets/cards/attack.png"
defense_card="assets/cards/defense.png"
curse_card="assets/cards/curse.png"
heal_card="assets/cards/heal.png"
back_card="assets/cards/back.png"

#罗马数字图片
num_1="assets/cards/1.png"
num_2="assets/cards/2.png"
num_3="assets/cards/3.png"
num_4="assets/cards/4.png"
num_5="assets/cards/5.png"
num_6="assets/cards/6.png"
num_7="assets/cards/7.png"
num_8="assets/cards/8.png"
num_9="assets/cards/9.png"
num_10="assets/cards/10.png"
num_11="assets/cards/11.png"
num_12="assets/cards/12.png"
num_13="assets/cards/13.png"
num_14="assets/cards/14.png"
num_15="assets/cards/15.png"
num_16="assets/cards/16.png"

#开始界面图片
TITLE_IMG = "assets/backgrounds/52.png"
TITLE_IMG_SIZE = (400* SCALE*3, 120* SCALE*6)  # 标题图片缩放尺寸
TITLE_IMG_OFFSET = (0, 40)   # 标题图片相对屏幕上方的偏移（x, y）

CLOUD1_IMG = "assets/backgrounds/cloud1.png"
CLOUD1_IMG_SIZE = (400* SCALE*4, 120* SCALE*8)  # 云朵图片缩放尺寸
CLOUD1_IMG_OFFSET = (40, 30)

CLOUD2_IMG = "assets/backgrounds/cloud2.png"
CLOUD2_IMG_SIZE = (1920, 900)  # 云朵2图片缩放尺寸
CLOUD2_IMG_OFFSET = (40, 30)  # 云朵2图片距离右下角的偏移（x, y）

eye_img="assets/backgrounds/eye.png"
eye_img_size=(1500, 800)
eye_img_offset = (0, 0)

STARS_IMG = "assets/backgrounds/stars.png"
STARS_IMG_SIZE = (SCREEN_WIDTH * SCALE/1.1 , SCREEN_HEIGHT* SCALE/1.1 )  # 星星图片缩放尺寸
STARS_IMG_OFFSET = (0, 0)  # 星星图片左上角相对屏幕的偏移（x, y）

NEW_GAME_IMG = "assets/backgrounds/new game.png"
START_BG_IMG = "assets/backgrounds/background.png"  # 背景图片
# 开始按钮图片尺寸
START_BTN_SIZE = (400* SCALE*2, 120* SCALE*4)
BTN_IMG = "assets/backgrounds/button.png"  # 开始按钮图片
LOADGAME_IMG = "assets/backgrounds/load game.png"  # load game字样图片
# load game字样图片相对按钮的偏移（x, y）
LOADGAME_TEXT_OFFSET = (0, -90)
LOADING_IMG = "assets/backgrounds/loading.png"
LOADING_DURATION = 2.5  # 加载动画时长（秒）
LOADING_IMG_SIZE = (1500, 800)  # 加载动画图片缩放尺寸


# 颜色定义
COLORS = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'GRAY': (200, 200, 200),
    'LIGHT_BLUE': (173, 216, 230),
    'YELLOW': (255, 255, 0)
}

# 卡牌类型颜色映射
CARD_COLORS = {
    'attack': (255, 100, 100),  # 红色系
    'defense': (100, 100, 255),  # 蓝色系
    'curse': (100, 100, 100),  # 灰色系
    'heal': (100, 255, 100)  # 绿色系
}

#卡牌尺寸
card_width = int(100 * SCALE)
card_height = int(150 * SCALE)
card_scale = SCALE
hover_scale = 1.0  # 悬停时略微放大

# 底部区域布局
bottom_area_height = 200

# 牌堆区域
pile_area_y = 30
#牌间距
card_spacing = int(40 * SCALE)

# 视觉效果
effect_duration= 1000 # 效果持续时间（毫秒）

# 牌选取判定区域边距
card_select_margin = 5

# 牌堆起始x坐标
pile_start_x = int(300 * SCALE)

# 数字图片在卡牌上的显示偏移（相对于卡牌左上角，单位像素）
NUM_IMAGE_OFFSET = (int(0.01 * card_width), int(6 * SCALE))  # (x_offset, y_offset)

# 数字图片缩放比例
NUM_IMAGE_SCALE = 1  # 1.0为原始大小，可根据需要调整

NUM_IMAGES = {
    1: num_1, 2: num_2, 3: num_3, 4: num_4, 5: num_5, 6: num_6, 7: num_7, 8: num_8,
    9: num_9, 10: num_10, 11: num_11, 12: num_12, 13: num_13, 14: num_14, 15: num_15, 16: num_16
}

# 结算区域参数
settlement_area_x = int(340 * SCALE)
settlement_area_y = screen_height - bottom_area_height + int(10 * SCALE)
settlement_area_width = int(750 * SCALE)
settlement_area_height = bottom_area_height - int(20 * SCALE)

#游戏ui图
ui_back="assets/ui/back2.png"
ui_settlement="assets/ui/back3.png"
ui_background="assets/ui/back.png"
ui_blood="assets/ui/Blood.png"
ui_bottleBack="assets/ui/Bottle1.png"
ui_bottlefront="assets/ui/Bottle2.png"
ui_front="assets/ui/Front.png"
ui_headL="assets/ui/Head1.png"
ui_headR="assets/ui/Head2.png"

# UI图片统一管理字典（含显示坐标和缩放比例）
UI_IMAGES = {
    "background": {"path": ui_background, "pos": (0, 0), "scale": 0.9},
    "back": {"path": ui_back, "pos": (0, -70), "scale": 0.9},
    "settlement": {"path": ui_settlement, "pos": (0, -70), "scale": 0.9},
    "bottleBack": {"path": ui_bottleBack, "pos": (50, 500), "scale": 0.7},
    "blood": {"path": ui_blood, "pos": (50, 500), "scale": 0.7},
    "bottlefront": {"path": ui_bottlefront, "pos": (50, 500), "scale": 0.7},
    "front": {"path": ui_front, "pos": (0, 0), "scale": 0.85},
    "headL": {"path": ui_headL, "pos": (0, 0), "scale": 0.9},
    "headR": {"path": ui_headR, "pos": (-120,0), "scale": 0.9},

}

# 血量上限
MAX_HEALTH = 10  # 可根据需要修改

# 血量数值显示参数
HP_FONT_SIZE = 32  # 字体大小
HP_COLOR = (220, 20, 60)  # 红色
HP_POS = (160, SCREEN_HEIGHT - 450)  # 左下角偏移








