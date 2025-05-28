# 卡牌类型
CARD_TYPES = ['attack', 'defense', 'curse', 'heal']

# 卡牌数值范围
CARD_VALUES = list(range(1, 11))  # 1-10

#屏幕大小
screen_width = 1200
screen_height = 800

#卡牌图片
attack_card="assets/cards/attack.png"
defense_card="assets/cards/defense.png"
curse_card="assets/cards/curse.png"
heal_card="assets/cards/heal.png"
back_card="assets/cards/back.png"

#罗马数字
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
card_width = 100
card_height = 150
card_scale = 1.0
hover_scale = 1.2

# 底部区域布局
bottom_area_height = 200

# 牌堆区域
pile_area_y = 50
#牌间距
card_spacing = 40

# 视觉效果
effect_duration= 1000 # 效果持续时间（毫秒）

# 牌选取判定区域边距
card_select_margin = 5

# 牌堆起始x坐标
pile_start_x = 50

