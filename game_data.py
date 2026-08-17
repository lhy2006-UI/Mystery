# -*- coding: utf-8 -*-
"""游戏数据：厉鬼、物品、地点、离线事件"""

GHOSTS = {
    '鬼眼': {'name': '鬼眼', 'level': '强鬼级', 'danger': 'B',
             'pattern': '六只眼睛分布全身，可开启鬼域透视',
             'abilities': ['鬼域', '透视', '化虹'], 'risk': 2},
    '无头鬼影': {'name': '无头鬼影', 'level': '强鬼级', 'danger': 'B',
                 'pattern': '后背面向它则被搬下头颅',
                 'abilities': ['鬼影攻击', '修改记忆', '死机'], 'risk': 3},
    '鬼绳': {'name': '鬼绳', 'level': '中鬼级', 'danger': 'C',
             'pattern': '碰到吊绳瞬间吊死', 'abilities': ['绞杀', '束缚'], 'risk': 2},
    '鬼差': {'name': '鬼差', 'level': '源头鬼级', 'danger': 'S',
             'pattern': '压制数>现场鬼数则瞬杀，吞噬成长，可重启',
             'abilities': ['压制', '重启', '吞噬'], 'risk': 5, 'divine': True},
    '饿死鬼': {'name': '饿死鬼', 'level': '源头鬼级', 'danger': 'S',
               'pattern': '五阶段进化规律', 'abilities': ['吞噬进化', '阴霾鬼域'], 'risk': 5},
    '替死鬼': {'name': '替死鬼', 'level': '恐怖级', 'danger': 'A',
               'pattern': '可转移伤害和死亡', 'abilities': ['转移伤害', '替死'], 'risk': 1},
    '鬼报纸': {'name': '鬼报纸', 'level': '中鬼级', 'danger': 'C',
               'pattern': '篡改记忆攻击最近的人', 'abilities': ['篡改记忆'], 'risk': 2},
    '鬼雾': {'name': '鬼雾', 'level': '中鬼级', 'danger': 'B',
             'pattern': '根据动静锁定，不动可活', 'abilities': ['浓雾', '同化'], 'risk': 2},
    '敲门鬼': {'name': '敲门鬼', 'level': '恐怖级', 'danger': 'A',
               'pattern': '三长两短敲门声，开门即死',
               'abilities': ['敲门即死', '鬼域'], 'risk': 3},
    '鬼婴': {'name': '鬼婴', 'level': '强鬼级', 'danger': 'B',
             'pattern': '只杀成年人，体内成长', 'abilities': ['鬼域冲击', '寄生'], 'risk': 3},
    '骗人鬼': {'name': '骗人鬼', 'level': '中鬼级', 'danger': 'C',
               'pattern': '伪装成熟人诱骗', 'abilities': ['伪装', '欺诈'], 'risk': 2},
    '鬼橱': {'name': '鬼橱', 'level': '恐怖级', 'danger': 'A',
             'pattern': '交易实现愿望，代价惨重',
             'abilities': ['愿望交易', '空间'], 'risk': 3},
    '鬼镜': {'name': '鬼镜', 'level': '强鬼级', 'danger': 'B',
             'pattern': '镜中留影可复活', 'abilities': ['镜像复活', '反射'], 'risk': 2},
    '鬼画': {'name': '鬼画', 'level': '恐怖级', 'danger': 'A',
             'pattern': '将人拖入画中世界', 'abilities': ['画中世界', '封印'], 'risk': 3},
    '鬼来电': {'name': '鬼来电', 'level': '中鬼级', 'danger': 'C',
               'pattern': '接听电话即被诅咒', 'abilities': ['电话诅咒'], 'risk': 2},
    '梦魇': {'name': '梦魇', 'level': '强鬼级', 'danger': 'B',
             'pattern': '入梦杀人，梦中死即真死',
             'abilities': ['梦境入侵', '精神攻击'], 'risk': 3},
    '哭坟鬼': {'name': '哭坟鬼', 'level': '中鬼级', 'danger': 'C',
               'pattern': '哭声引来死亡', 'abilities': ['哭声诅咒'], 'risk': 2},
    '干尸新娘': {'name': '干尸新娘', 'level': '强鬼级', 'danger': 'B',
                 'pattern': '寻找新郎，被选中者死',
                 'abilities': ['鬼婚', '诅咒'], 'risk': 3},
    '鬼掐人': {'name': '鬼掐人', 'level': '弱鬼级', 'danger': 'C',
               'pattern': '无形之手掐脖子', 'abilities': ['远程扼杀'], 'risk': 1},
    '鬼食人': {'name': '鬼食人', 'level': '强鬼级', 'danger': 'B',
               'pattern': '吞噬活人成长', 'abilities': ['吞噬', '肉体强化'], 'risk': 3},
    '血衣鬼': {'name': '血衣鬼', 'level': '强鬼级', 'danger': 'B',
               'pattern': '血衣沾染即被诅咒', 'abilities': ['血咒', '寄生'], 'risk': 3},
    '井鬼': {'name': '井鬼', 'level': '中鬼级', 'danger': 'C',
             'pattern': '井中爬出拖人入水', 'abilities': ['水鬼拖入'], 'risk': 2},
    '童鬼': {'name': '童鬼', 'level': '中鬼级', 'danger': 'C',
             'pattern': '孩童形态引人怜悯后猎杀',
             'abilities': ['伪装', '群体猎杀'], 'risk': 2},
    '刘老太': {'name': '刘老太', 'level': '恐怖级', 'danger': 'A',
               'pattern': '墓园控制死者', 'abilities': ['尸群控制', '墓地鬼域'], 'risk': 3},
}

ITEMS = {
    '人皮纸': {'name': '人皮纸', 'desc': '展开鬼域，提供信息但会欺诈', 'type': '特殊'},
    '棺材钉': {'name': '棺材钉', 'desc': '限制关押鬼的行动', 'type': '关押'},
    '红色鬼烛': {'name': '红色鬼烛', 'desc': '点燃后鬼无法进入烛光范围', 'type': '防御'},
    '白色鬼烛': {'name': '白色鬼烛', 'desc': '点燃吸引所有鬼仇恨', 'type': '战术'},
    '鬼镜': {'name': '鬼镜', 'desc': '复活镜中留影之人', 'type': '复活'},
    '柴刀': {'name': '柴刀', 'desc': '肢解灵异，高伤害', 'type': '攻击'},
    '鬼瓷': {'name': '鬼瓷', 'desc': '抵挡鬼袭击直至碎裂', 'type': '防御'},
    '黄金': {'name': '黄金', 'desc': '压制厉鬼复苏', 'type': '材料'},
    '队长令牌': {'name': '队长令牌', 'desc': '队长级证明', 'type': '身份'},
    '神位碎片': {'name': '神位碎片', 'desc': '黄金门后掉落的神物', 'type': '神物'},
}

LOCATIONS = [
    {'id': 'school', 'name': '第七高中', 'desc': '敲门鬼事件发生地', 'danger': 'A'},
    {'id': 'mall', 'name': '富仁商场', 'desc': '无头鬼影出没', 'danger': 'B'},
    {'id': 'village', 'name': '黄岗村', 'desc': '荒废村庄，鬼差诞生地', 'danger': 'S'},
    {'id': 'temple', 'name': '弘法寺', 'desc': '镇压厉鬼的寺庙', 'danger': 'B'},
    {'id': 'hotel', 'name': '凯撒大酒店', 'desc': '多重鬼域叠加', 'danger': 'A'},
    {'id': 'postoffice', 'name': '鬼邮局', 'desc': '重叠空间，送信任务', 'danger': 'A'},
    {'id': 'cemetery', 'name': '福寿园墓园', 'desc': '刘老太出没', 'danger': 'B'},
    {'id': 'safehouse', 'name': '观江小区', 'desc': '黄金安全屋', 'danger': 'C'},
    {'id': 'street', 'name': '大昌市街道', 'desc': '随机灵异事件', 'danger': 'B'},
    {'id': 'mansion', 'name': '民国古宅', 'desc': '鬼镜鬼橱所在', 'danger': 'A'},
    {'id': 'oldtown', 'name': '旧城遗址', 'desc': '被灵异吞噬的旧城区', 'danger': 'A'},
]

STAGES = ['普通人', '新手驭鬼者', '成熟驭鬼者', '队长级', '源头级', '神级']

# 序章剧情
PROLOGUE = [
    {
        'narration': '晚自习的铃声刚响过，第七高中高三教室的灯忽然闪烁了一下。你叫杨间，是这所学校的普通高三学生。窗外的天色青得诡异。\n\n"同学们安静一下。"班主任走进来，"今天有国际刑警的周正同志来做安全讲座。"\n\n一个穿黑色风衣的男人走上讲台，他的眼神锐利得不像普通人，一直盯着教室门。',
        'choices': [
            {'text': '认真听周正讲话', 'risk': 'low'},
            {'text': '趴在桌上睡觉', 'risk': 'medium'},
            {'text': '观察教室周围的异常', 'risk': 'low'},
        ]
    },
    {
        'narration': '讲座刚讲一半，教室门外忽然传来敲门声。\n\n咚——咚——咚——\n咚——咚——\n\n三长两短。\n\n周正脸色骤变："所有人！不要开门！不要出声！"\n\n青黑色雾气从门缝渗进来，温度骤降。你的同学方镜脸色惨白，忽然站起来朝门走去。',
        'choices': [
            {'text': '拉住方镜阻止他', 'risk': 'medium'},
            {'text': '躲到讲台后面', 'risk': 'low'},
            {'text': '从教室后门溜出去', 'risk': 'high'},
        ]
    },
    {
        'narration': '你没能拉住方镜。他猛地拉开门——门外站着一个高瘦长衫老人，面色灰白，眼睛是两个黑洞。\n\n方镜只看了一眼就倒了下去。周正怒吼着放出鬼域和鬼婴对抗敲门鬼。\n\n混乱中，方镜忽然从地上爬起，手里攥着人皮纸，眼神冰冷地推了你一把。你摔进了走廊尽头的厕所——那是另一个空间。',
        'choices': [
            {'text': '探索这个诡异空间', 'risk': 'medium'},
            {'text': '尝试打开厕所门出去', 'risk': 'high'},
        ]
    },
    {
        'narration': '厕所隔间无限延伸，墙壁上长满眼睛。最深处，一个被锁链束缚的巨大存在全身都长着眼睛，正盯着你——鬼眼之主。\n\n你肚子剧痛，皮肤裂开，六只鬼眼从伤口挤出，分布在你全身。你驾驭了鬼眼！\n\n你捡起人皮纸，用鬼眼+人皮纸的力量打开通道。回到教室时周正已死，鬼婴复苏只杀成年人。你带着幸存同学逃离了第七高中。',
        'choices': [{'text': '进入大昌市，成为驭鬼者', 'risk': 'low'}],
        'effects': {'insight': 10},
        'rewards': {'ghost': '鬼眼', 'item': '人皮纸'}
    },
]

# 离线事件库
OFFLINE_EVENTS = {
    '第七高中': [
        {'name': '废弃教室', 'desc': '你回到了第七高中，教室里还残留着敲门鬼的气息。课桌上散落着未完成的试卷。',
         'effects': {'insight': 8}},
        {'name': '鬼婴残留', 'desc': '走廊深处传来婴儿的啼哭声，周正死后鬼婴曾在此游荡。',
         'effects': {'sanity': -10}, 'ghost': '鬼婴'},
        {'name': '方镜的座位', 'desc': '你找到了方镜的座位，抽屉里有一张泛黄的照片，照片上的方镜眼睛是两个黑洞。',
         'effects': {'insight': 10, 'sanity': -5}},
    ],
    '富仁商场': [
        {'name': '空荡的商场', 'desc': '深夜的富仁商场空无一人，自动扶梯还在运行。你听到楼上传来无头的脚步声。',
         'effects': {'insight': 6}, 'ghost': '无头鬼影'},
        {'name': '严力的办公室', 'desc': '商场经理办公室里，你找到了严力的档案。他曾是国际刑警，后来驾驭了无头鬼影。',
         'effects': {'insight': 12}},
    ],
    '黄岗村': [
        {'name': '荒废祠堂', 'desc': '祠堂里有一具穿清朝官服的干尸，手握生锈令牌。它似乎在沉睡。',
         'effects': {'insight': 12}},
        {'name': '鬼棺', 'desc': '一口黑棺横在路中，棺盖刻满符文。里面有东西在敲打棺壁。',
         'effects': {'sanity': -12}, 'ghost': '童鬼'},
        {'name': '枯井', 'desc': '村中央的枯井深不见底，你往井里看时，看到井底有一双眼睛在看你。',
         'effects': {'sanity': -15, 'insight': 10}},
        {'name': '村长家', 'desc': '破败的村长家里，你找到了一本日记，记载着黄岗村曾因一场瘟疫全村死亡。',
         'effects': {'insight': 15}},
    ],
    '弘法寺': [
        {'name': '大雄宝殿', 'desc': '寺庙的佛像都被破坏了，你在佛像底座下发现了棺材钉。',
         'effects': {'insight': 8}, 'item': '棺材钉'},
        {'name': '藏经阁', 'desc': '藏经阁里的经书全部变成了空白，只有一本写满了厉鬼的名字和规律。',
         'effects': {'insight': 15}},
    ],
    '凯撒大酒店': [
        {'name': '酒店大堂', 'desc': '酒店大堂的水晶灯在摇晃，前台没有人，但入住登记本上写满了名字。',
         'effects': {'insight': 8}, 'ghost': '鬼画'},
        {'name': '总统套房', 'desc': '套房里的镜子全部被打碎了，你在浴缸里发现了鬼镜。',
         'effects': {'insight': 10}, 'item': '鬼镜'},
    ],
    '鬼邮局': [
        {'name': '邮局大厅', 'desc': '民国风格的邮局里，信件在自动分类。柜台上放着一封写给你的信。',
         'effects': {'insight': 10}},
        {'name': '信使', 'desc': '一个穿民国制服的信使走向你，它的脸是空白的。"你的信。"它说。',
         'effects': {'sanity': -10}, 'ghost': '鬼报纸'},
    ],
    '福寿园墓园': [
        {'name': '墓碑林', 'desc': '无数墓碑排列整齐，你发现其中一块墓碑上刻着你的名字和今天的日期。',
         'effects': {'sanity': -20, 'insight': 15}},
        {'name': '刘老太', 'desc': '一个驼背老太太坐在坟前烧纸，她抬起头，眼睛是两个黑洞。',
         'effects': {'sanity': -15}, 'ghost': '刘老太'},
        {'name': '陪葬品', 'desc': '你在一个被盗的墓里发现了红色鬼烛。',
         'effects': {'insight': 5}, 'item': '红色鬼烛'},
    ],
    '观江小区': [
        {'name': '黄金安全屋', 'desc': '你回到了黄金安全屋，黄金的墙壁压制着体内的厉鬼。',
         'effects': {'health': 30, 'sanity': 20, 'revival': -15}},
        {'name': '监控室', 'desc': '安全屋的监控显示着大昌市各处的灵异活动。',
         'effects': {'insight': 10}},
        {'name': '地下室', 'desc': '地下室里存放着黄金和灵异物品，你找到了鬼瓷。',
         'effects': {'health': 15}, 'item': '鬼瓷'},
    ],
    '大昌市街道': [
        {'name': '空无一人', 'desc': '街道上空无一人，只有你自己的脚步声。路灯在闪烁。',
         'effects': {'insight': 6}},
        {'name': '灵异残留', 'desc': '你发现了一处刚发生过灵异事件的现场，地上只有衣物没有尸体。',
         'effects': {'insight': 10}},
        {'name': '遭遇厉鬼', 'desc': '一只厉鬼忽然从阴影中出现！', 'ghost': 'random'},
        {'name': '电话亭', 'desc': '一个废弃电话亭里的电话忽然响了。你接起来，听到了自己的声音。',
         'effects': {'sanity': -12}, 'ghost': '鬼来电'},
    ],
    '民国古宅': [
        {'name': '古宅大门', 'desc': '民国风格的古宅大门敞开着，门环上挂着一面铜镜。',
         'effects': {'insight': 12, 'sanity': -8}},
        {'name': '鬼橱', 'desc': '你在密室里发现了鬼橱，它可以实现愿望，但代价是你最珍贵的东西。',
         'effects': {'sanity': -10}, 'ghost': '鬼橱'},
        {'name': '张伟的房间', 'desc': '你找到了张伟的房间，桌上有他的笔记。',
         'effects': {'insight': 15}},
    ],
    '旧城遗址': [
        {'name': '废墟', 'desc': '旧城被灵异吞噬后变成了废墟，建筑扭曲变形。',
         'effects': {'insight': 8, 'sanity': -8}},
        {'name': '扭曲空间', 'desc': '你走进了一个扭曲的空间，上下左右都失去了意义。',
         'effects': {'sanity': -15, 'insight': 12}},
        {'name': '沉睡的鬼', 'desc': '废墟深处沉睡着一只强大的厉鬼，你不小心惊醒了它。',
         'ghost': 'random'},
    ],
}
