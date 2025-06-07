# 卡牌类型
CARD_TYPES = ['attack', 'defense', 'curse', 'heal']

# 卡牌数值范围
CARD_VALUES = list(range(1, 17))  # 1-16

# 屏幕基准分辨率（原设计）
BASE_WIDTH = 1200
BASE_HEIGHT = 800
# 目标分辨率
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
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
title_img="assets/backgrounds/52.png"
titleBackground_img="assets/backgrounds/background.png"
button_img="assets/images/button.png"
cloud1_img="assets/images/cloud1.png"
cloud2_img="assets/images/cloud2.png"
eye_img="assets/images/eye.png"
loadGame_img="assets/backgrounds/load game.png"
loading_img="assets/images/loading.png"
new_game_img="assets/backgrounds/new game.png"
stars_img="assets/images/stars.png"


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
hover_scale = 1.0 * SCALE  # 悬停时略微放大

# 底部区域布局
bottom_area_height = 200

# 牌堆区域
pile_area_y = 50
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



