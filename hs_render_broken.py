from PIL import Image, ImageDraw, ImageFont
import math
import os
import time

# 基于「就这水平的thsd」的PS模板(v4.2)制作 https://www.iyingdi.com/tz/post/5062456
# 先做显式版
# 再做枚举版
# import hearthstone.deckstrings
# https://github.com/HearthSim/python-hearthstone/blob/master/hearthstone/enums.py


font_1_p = os.sep.join(('font', 'GLEI00M_t.ttf'))
font_2_p = os.sep.join(('font', 'BlizzardGlobal.ttf'))  # 暴黑
font_2b_p = os.sep.join(('font', 'BlizzardGlobal-Bold.ttf'))  # 暴黑加粗
font_1_26 = ImageFont.truetype(font=font_1_p, size=26, index=0)  # （备用）缩小牌名
font_1_32 = ImageFont.truetype(font=font_1_p, size=32, index=0)  # 类别标签
font_1_34 = ImageFont.truetype(font=font_1_p, size=34, index=0)  # 标准牌名
font_1_106 = ImageFont.truetype(font=font_1_p, size=106, index=0)  # 攻击力 生命值
font_1_116 = ImageFont.truetype(font=font_1_p, size=116, index=0)  # 费用
font_2_100 = ImageFont.truetype(font=font_2_p, size=100, index=0)  #
font_2b_100 = ImageFont.truetype(font=font_2b_p, size=100, index=0)

minion_art_mask_p = os.sep.join(('normal', 'art_mask.png'))
minion_name_bar_p = os.sep.join(('normal', 'name_frame.png'))
minion_gem_bar_p = os.sep.join(('normal', 'gem_frame.png'))
gem_1_p = os.sep.join(('normal', 'gem_1.png'))
gem_3_p = os.sep.join(('normal', 'gem_3.png'))
gem_4_p = os.sep.join(('normal', 'gem_4.png'))
gem_5_p = os.sep.join(('normal', 'gem_5.png'))
dragon_p = os.sep.join(('normal', 'dragon.png'))
text_bar_p = os.sep.join(('normal', 'text_bar.png'))
tag_bar_p = os.sep.join(('normal', 'tag_bar.png'))
atk_1_p = os.sep.join(('normal', 'atk_1.png'))
atk_2_p = os.sep.join(('normal', 'atk_2.png'))
hp_1_p = os.sep.join(('normal', 'hp_1.png'))
hp_2_p = os.sep.join(('normal', 'hp_2.png'))
hp_3_p = os.sep.join(('normal', 'hp_3.png'))
cost_1_p = os.sep.join(('normal', 'cost_1.png'))
cost_2_p = os.sep.join(('normal', 'cost_2.png'))
# cost_3.png ~ cost_11.png
star_0_p = os.sep.join(('normal', 'star_0.png'))
flag_0_p = os.sep.join(('normal', 'flag_0.png'))

clazz_range = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
clazz_n = [None] * 15
for i in clazz_range:
    _p = os.sep.join(('normal', 'clazz_' + str(i) + '.png'))
    with Image.open(_p) as _i:
        clazz_n[i] = Image
        print(type(_i))
        

clazz_sep_p = os.sep.join(('normal', 'clazz_sep.png'))
clazz_range_2 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14)
clazz_l_n = [None] * 15
for i in clazz_range_2:
    _p = os.sep.join(('normal', 'clazz_l_' + str(i) + '.png'))
    with Image.open(_p) as _i:
        clazz_l_n[i] = _i
clazz_r_n = [None] * 15
for i in clazz_range_2:
    _p = os.sep.join(('normal', 'clazz_r_' + str(i) + '.png'))
    with Image.open(_p) as _i:
        clazz_r_n[i] = _i


def minion_x2yz(x):
    y = 345 - int(math.sin((x - 230) / 220 * math.pi) * 13)
    z = - math.cos((x - 230) / 220 * math.pi) * 13
    return y, z


def hs_render(
    name='名称',  # text
    cardtype=0,  # 英雄/英雄牌 随从 法术 武器 技能 3 4 5 7 10
    clazz=None,  # [0], [10], [0,1] 1-10 死德猎法骑牧贼萨术战 None=12 中立 14 瞎 11 梦境 13 威兹班
    rarity=2,  # NCREL 21345
    dragon=False,  # T/F
    tag=None,  # text
    text='规则文本',
    star=0,  # 战棋随从为1-6
    cost=None,
    # cost_b=1,  # 费用背景 战棋=2 目前自动
    cost_h=False,  # 隐藏费用
    atk=0,
    atk_h=False,  # 隐藏攻击
    hp=0,
    hp_h=False,  # 隐藏生命
    # watermark=None,  # 系列编号 等待更新
    flag=None,  # 交易[0], 污手党[1], 暗金教[2], 玉莲帮[3], 双职业[2,9], 三职业[2,9,14], 四职业[2,3,4,9]
    art_path='default.png'
):
    if clazz is None:
        clazz = [12]
    img = Image.new('RGBA', (536, 670))
    d = ImageDraw.Draw(img)

    if cardtype == 3:  # 英雄/英雄牌
        pass
    elif cardtype == 4:  # 随从
        with Image.open(art_path) as art_img:
            art_img = art_img.convert('RGBA').resize((332, 332))
            poly = [(0, 0), (0, 90), (55, 90), (99, 20), (144, 0)]
            ImageDraw.Draw(art_img).polygon(poly, outline=(255, 255, 255, 0), fill=(255, 255, 255, 0))
            poly = [(332, 0), (332, 90), (277, 90), (233, 20), (188, 0)]
            ImageDraw.Draw(art_img).polygon(poly, outline=(255, 255, 255, 0), fill=(255, 255, 255, 0))
            img.paste(art_img, (102, 78), mask=art_img)
        with Image.open(minion_art_mask_p) as art_mask:
            img.paste(art_mask, (152, 84), mask=art_mask)

        if len(clazz) == 1:
            k = clazz[0]
            img.paste(clazz_n[k], (77, 68), mask=clazz_n[k])
        elif len(clazz) == 2:
            k = clazz[0]
            img.paste(clazz_l_n[k], (77, 68), mask=clazz_l_n[k])
            k = clazz[1]
            img.paste(clazz_r_n[k], (268, 68), mask=clazz_r_n[k])
            with Image.open(clazz_sep_p) as clazz_sep:
                img.paste(clazz_sep, (260, 417), mask=clazz_sep)
        else:
            clazz0_p = os.sep.join(('normal', 'clazz_12.png'))
            with Image.open(clazz0_p) as clazz0:
                img.paste(clazz0, (77, 68), mask=clazz0)
        with Image.open(minion_name_bar_p) as name_frame:
            img.paste(name_frame, (94, 343), mask=name_frame)
        with Image.open(text_bar_p) as text_bar:
            img.paste(text_bar, (104, 427), mask=text_bar)
        if tag:
            with Image.open(tag_bar_p) as tag_bar:
                img.paste(tag_bar, (163, 585), mask=tag_bar)

        d.text((268, 587), tag, fill='white', anchor='ma', font=font_1_32, align='center', stroke_width=2,
               stroke_fill='black')

        if rarity > 0:
            with Image.open(minion_gem_bar_p) as gem_frame:
                img.paste(gem_frame, (225, 395), mask=gem_frame)
            if rarity == 1:
                with Image.open(gem_1_p) as gem_1:
                    img.paste(gem_1, (259, 405), mask=gem_1)
            elif rarity == 3:
                with Image.open(gem_3_p) as gem_3:
                    img.paste(gem_3, (259, 405), mask=gem_3)
            elif rarity == 4:
                with Image.open(gem_4_p) as gem_4:
                    img.paste(gem_4, (259, 405), mask=gem_4)
            elif rarity == 5:
                with Image.open(gem_5_p) as gem_5:
                    img.paste(gem_5, (259, 405), mask=gem_5)
        if dragon:
            with Image.open(dragon_p) as dragon:
                img.paste(dragon, (161, 42), mask=dragon)

        if atk_h:
            pass
        else:
            with Image.open(atk_1_p) as atk_1:
                img.paste(atk_1, (51, 527), mask=atk_1)
            # with Image.open(atk_2_p) as atk_2:
            #     img.paste(atk_2, (51, 527), mask=atk_2)
            d.text((116, 540), str(atk), fill='white', anchor='ma', font=font_1_106, align='center', stroke_width=3,
                   stroke_fill='black')

        if hp_h:
            pass
        else:
            with Image.open(hp_1_p) as hp_1:
                img.paste(hp_1, (385, 532), mask=hp_1)
            # with Image.open(hp_2_p) as hp_2:
            #     img.paste(hp_2, (385, 532), mask=hp_2)
            # with Image.open(hp_3_p) as hp_3:
            #     img.paste(hp_3, (385, 532), mask=hp_3)
            d.text((430, 542), str(hp), fill='white', anchor='ma', font=font_1_106, align='center', stroke_width=3,
                   stroke_fill='black')

        if star > 0:
            with Image.open(star_0_p) as star_0:
                img.paste(star_0, (60, 77), mask=star_0)
            star_p = os.sep.join(('normal', 'star_' + str(star) + '.png'))
            with Image.open(star_p) as star:
                img.paste(star, (60, 77), mask=star)
        else:
            with Image.open(cost_1_p) as cost_1:
                img.paste(cost_1, (42, 57), mask=cost_1)
        if cost_h:
            pass
        else:
            d.text((109, 64), str(cost), fill='white', anchor='ma', font=font_1_116, align='center', stroke_width=3,
                   stroke_fill='black')
        if flag:
            if len(flag) == 1:
                flag_p = os.sep.join(('normal', 'flag_' + str(flag[0]) + '.png'))
                with Image.open(flag_p) as flag:
                    img.paste(flag, (63, 88), mask=flag)
            elif len(flag) == 2:
                pass
            elif len(flag) == 3:
                pass
            elif len(flag) == 4:
                pass

        name_img_check = [z1(ch) for ch in name]
        ch_len = sum([x[1] for x in name_img_check])
        x = 276 - ch_len // 2
        for ch_img_check in name_img_check:
            y, z = minion_x2yz(x)
            img_rotated = ch_img_check[0].rotate(-z, resample=Image.BICUBIC)
            img.paste(img_rotated, (x - ch_img_check[1] // 2, y + 19), mask=img_rotated)
            x += ch_img_check[1]

        # 分行函数下次写
        lines = text.split('\n')
        if len(lines) < 5:
            y = 460
            for i, line in enumerate(lines):
                text_img_check = [zb(ch) for ch in line]
                ch_len = sum([17 if x[1] else 29 for x in text_img_check])
                x = 268 - ch_len // 2
                for ch_img_check in text_img_check:
                    img.paste(ch_img_check[0], (x, y), mask=ch_img_check[0])
                    x += 17 if ch_img_check[1] else 29
                y += 31
    elif cardtype == 5:  # 法术
        pass
    elif cardtype == 7:
        pass
    elif cardtype == 10:
        pass
    img.save('G1.png')


def break_lines(text):
    raw_lines = text.split('\n')
    detailed_lines = []
    for line in raw_lines:
        bold = []
        line = line.replace('<i>', '').replace('</i>', '').replace('$', '').replace('#', '', 0)
        while '<b>' in line or '</b>' in line:
            start = max(line.find('<b>'), 0)
            line = line.replace('<b>', '', 1)
            end = line.find('</b>')
            if end == -1:
                end = len(line)
            bold += range(start, end)
            line = line.replace('</b>', '', 1)
        detailed_lines.append((line, bold))
    if len(detailed_lines) == 1:
        if len(detailed_lines[0][0]) < 10:
            return detailed_lines
        if len(detailed_lines[0][0]) < 21:
            if detailed_lines[0][0][10] not in ('，', '。', '：'):
                work = [(detailed_lines[0][0][:10], [x in detailed_lines[0][1] for x in range(10)])]
                print(work)


def main():
    # main(cardtype=5, rarity=4, clazz=[9], dragon=True, typa='野兽', art_path='G.png')
    aa = {
        'name': '高弗雷先辈',
        'text': '规则文本，十个字注意\n规则文本，2个字注意\n换行这里八个字了\n然后结束。',
        'cardtype': 4,
        'rarity': 5,
        'clazz': [9],
        'dragon': True,
        'tag': '野兽',
        'cost': 7,
        'atk': 4,
        'hp': 4,
        'flag': [0],
        'art_path': 'default.png'
    }
    hs_render(**aa)


def z1(c='爱', s=36, f=font_1_34):
    _check = c.isascii()
    img = Image.new('RGBA', (0, 0))
    d = ImageDraw.Draw(img)
    tx = d.textsize(c, f)
    if _check:
        w = tx[0] + 4
    else:
        w = s
    img = Image.new('RGBA', (w, s))
    d = ImageDraw.Draw(img)
    d.text((w // 2, 0), c, font=f, anchor='ma', fill='white', stroke_width=3, stroke_fill='black')
    # d.polygon([(0, 0), (0, s), (s, s), (s, 0)], outline='black')
    return img, w


def zb(c='爱', s=28, width=0):
    _x = int(s * 0.56)
    _c = c.encode('utf-8')
    _check = _c.isalpha() or _c.isdigit()
    if _check:
        img = Image.new('RGBA', (56, 100))
    else:
        img = Image.new('RGBA', (100, 100))
    d = ImageDraw.Draw(img)
    # offset = font_b_100.getoffset(c)
    if _check:
        a = 28
    else:
        a = 50
    d.text((a, 50), c, anchor='mm', font=font_2_100, fill='black',
           stroke_width=width, stroke_fill='black')
    if _check:
        im2 = img.resize((_x, s))
    else:
        im2 = img.resize((s, s))
    return im2, _check


def test():
    # ll = '<b>突袭</b>，<b>超杀</b>：从你的牌库中抽一张法术牌。'
    # break_lines(ll)
    a = '测试，本1啊+2/+1！'
    c_c = [z1(c) for c in a]
    for cc in c_c:
        pass
    

if __name__ == "__main__":
    t = time.time()
    main()
    print(time.time() - t)
    # test()
    
