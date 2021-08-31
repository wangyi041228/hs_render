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

font_2_18 = ImageFont.truetype(font=font_2_p, size=18, index=0)
font_2b_18 = ImageFont.truetype(font=font_2b_p, size=18, index=0)
font_2_20 = ImageFont.truetype(font=font_2_p, size=20, index=0)
font_2b_20 = ImageFont.truetype(font=font_2b_p, size=20, index=0)
font_2_26 = ImageFont.truetype(font=font_2_p, size=26, index=0)
font_2b_26 = ImageFont.truetype(font=font_2b_p, size=26, index=0)
font_2_28 = ImageFont.truetype(font=font_2_p, size=28, index=0)
font_2b_28 = ImageFont.truetype(font=font_2b_p, size=28, index=0)
font_2_32 = ImageFont.truetype(font=font_2_p, size=32, index=0)
font_2b_32 = ImageFont.truetype(font=font_2b_p, size=32, index=0)
_i_ = Image.new('RGBA', (0, 0))
_d_ = ImageDraw.Draw(_i_)


def ini(p):
    with Image.open(p) as _img:
        img = Image.new('RGBA', _img.size)
        img.paste(_img)
        return img


minion_art_mask_p = os.sep.join(('normal', 'art_mask.png'))
minion_art_mask = ini(minion_art_mask_p)
minion_name_bar_p = os.sep.join(('normal', 'name_frame.png'))
minion_name_bar = ini(minion_name_bar_p)
text_bar_p = os.sep.join(('normal', 'text_bar.png'))
text_bar = ini(text_bar_p)
tag_bar_p = os.sep.join(('normal', 'tag_bar.png'))
tag_bar = ini(tag_bar_p)

minion_gem_bar_p = os.sep.join(('normal', 'gem_frame.png'))
minion_gem_bar = ini(minion_gem_bar_p)

gem_n = [Image.new('RGBA', (0, 0))] * 6
for i in (1, 3, 4, 5):
    gem_n[i] = ini(os.sep.join(('normal', 'gem_' + str(i) + '.png')))

dragon_crown_p = os.sep.join(('normal', 'dragon_crown.png'))
dragon_crown = ini(dragon_crown_p)

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

clazz_n = [Image.new('RGBA', (0, 0))] * 15
for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14):
    clazz_n[i] = ini(os.sep.join(('normal', 'clazz_' + str(i) + '.png')))

clazz_l_n = [Image.new('RGBA', (0, 0))] * 15
for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14):
    clazz_l_n[i] = ini(os.sep.join(('normal', 'clazz_l_' + str(i) + '.png')))
    
clazz_r_n = [Image.new('RGBA', (0, 0))] * 15
for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14):
    clazz_r_n[i] = ini(os.sep.join(('normal', 'clazz_r_' + str(i) + '.png')))
    
clazz_sep_p = os.sep.join(('normal', 'clazz_sep.png'))
clazz_sep = ini(clazz_sep_p)


def minion_x2yz(x: int):
    y = 345 - int(math.sin((x - 230) / 220 * math.pi) * 13)
    z = - math.cos((x - 230) / 220 * math.pi) * 13
    return y, z


def hs_render(
    name='名称',  # 牌名
    cardtype=4,  # 类别：英雄/英雄牌 随从 法术 武器 技能 3 4 5 7 10
    clazz=None,  # 职业：[0], [10], [0,1] 1-10 死德猎法骑牧贼萨术战 None=12 中立 14 瞎 11 梦境 13 威兹班
    rarity=2,  # 稀有度：NCREL 21345
    dragon=False,  # 传说龙框
    tag=None,  # 类别标签 随从法术通用
    text='规则文本',  # 规则文本
    star=0,  # 星级：战棋随从 1-6
    cost=0,  # 费用
    # cost_b=None,  # 费用背景 0=水晶 1=战棋铸币
    cost_hidden=False,  # 费用隐藏
    atk=0,  # 攻击力
    # atk_b=None,  # 攻击力背景 0=角色 1=武器
    atk_hidden=False,  # 攻击力隐藏
    hp=0,
    # hp_b=None,
    hp_hidden=False,  # 隐藏生命
    # watermark=None,  # 系列编号 等待更新
    flag=None,  # 交易[0], 污手党[1], 暗金教[2], 玉莲帮[3], 双职业[2,9], 三职业[2,9,14], 四职业[2,3,4,9]
    art_path='default.png'
):
    # 修正参数
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
        img.paste(minion_art_mask, (152, 84), mask=minion_art_mask)
        
        if len(clazz) == 1:
            k = clazz[0]
            img.paste(clazz_n[k], (77, 68), mask=clazz_n[k])
        elif len(clazz) == 2:
            k = clazz[0]
            img.paste(clazz_l_n[k], (77, 68), mask=clazz_l_n[k])
            k = clazz[1]
            img.paste(clazz_r_n[k], (268, 68), mask=clazz_r_n[k])
            img.paste(clazz_sep, (260, 417), mask=clazz_sep)
        else:
            k = 12
            img.paste(clazz_n[k], (77, 68), mask=clazz_n[k])

        img.paste(minion_name_bar, (94, 343), mask=minion_name_bar)
        img.paste(text_bar, (104, 427), mask=text_bar)
        if tag:
            img.paste(tag_bar, (163, 585), mask=tag_bar)
            d.text((268, 587), tag, fill='white', anchor='ma', font=font_1_32, align='center', stroke_width=2,
                   stroke_fill='black')

        if rarity > 0:
            img.paste(minion_gem_bar, (225, 395), mask=minion_gem_bar)
            img.paste(gem_n[rarity], (259, 405), mask=gem_n[rarity])

        if dragon:
            img.paste(dragon_crown, (161, 42), mask=dragon_crown)

        if atk_hidden:
            pass
        else:
            with Image.open(atk_1_p) as atk_1:
                img.paste(atk_1, (51, 527), mask=atk_1)
            
            d.text((116, 540), str(atk), fill='white', anchor='ma', font=font_1_106, align='center', stroke_width=3,
                   stroke_fill='black')
        
        if hp_hidden:
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
        if cost_hidden:
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
        if tag:
            tag_tf = 1
        else:
            tag_tf = 0
        out_lines = minion_break_lines(text, tag_tf)
        font_paras = [[None,
                       (font_2_32, font_2b_32, 32, 510),
                       (font_2_32, font_2b_32, 32, 490),
                       (font_2_28, font_2b_28, 28, 475),
                       (font_2_28, font_2b_28, 28, 460),
                       (font_2_20, font_2b_20, 22, 450)],
                      [None,
                       (font_2_28, font_2b_28, 30, 510),
                       (font_2_28, font_2b_28, 30, 495),
                       (font_2_26, font_2b_26, 28, 480),
                       (font_2_20, font_2b_20, 22, 470),
                       (font_2_18, font_2b_18, 20, 450)]]
        f_para = font_paras[tag_tf][len(out_lines)]
        f_a = f_para[0]
        f_b = f_para[1]
        f_size = f_para[2]
        y = f_para[3]
        for line in out_lines:
            text_img_check = [z2(line[0][_i], f_size, f_b) if _i in line[1] else z2(line[0][_i], f_size, f_a)
                              for _i in range(len(line[0]))]
            ch_len = sum([x[1] for x in text_img_check])
            x = 268 - ch_len // 2
            for ch_img_check in text_img_check:
                img.paste(ch_img_check[0], (x, y), mask=ch_img_check[0])
                x += ch_img_check[1]
            y += int(f_size * 1.1)
    elif cardtype == 5:  # 法术
        pass
    elif cardtype == 7:
        pass
    elif cardtype == 10:
        pass
    img.save('G1.png')


def minion_break_lines(text, t=False):
    if t:
        line_limit = [None,
                      [235],
                      [235, 235],
                      [275, 275, 275],
                      [315, 315, 315, 237],
                      [342, 342, 342, 262, 262],
                      [], ]
    else:
        line_limit = [None,
                      [235],
                      [235, 235],
                      [275, 275, 275],
                      [275, 275, 210, 160],
                      [315, 315, 315, 262, 262],
                      [], ]
    raw_lines = text.split('\n')
    detailed_lines = []
    for line in raw_lines:
        bold = []
        line = line.replace('<i>', '').replace('</i>', '').replace('$', '').replace('#', '')
        while '<b>' in line or '</b>' in line:
            start = max(line.find('<b>'), 0)
            line = line.replace('<b>', '', 1)
            end = line.find('</b>')
            if end == -1:
                end = len(line)
            bold += range(start, end)
            line = line.replace('</b>', '', 1)
        detailed_lines.append((line, bold))
    print(detailed_lines)
    line_result = 0
    line_all = len(detailed_lines)
    f_try = font_2_26  # 28 16
    x_lists = [[_d_.textsize(c, f_try)[0] for c in detailed_lines[ll][0]] for ll in range(line_all)]
    print(x_lists)
    if line_all == 1:
        x_list = x_lists[0]
        if sum(x_list) < 235:
            line_result = 1
    if line_result == 0 and len(detailed_lines) < 3:
        if sum([int(math.ceil(sum(x_lists[ll]) / 235)) for ll in range(line_all)]) < 3:
            line_result = 2
    if line_result == 0 and len(detailed_lines) < 4:
        if sum([int(math.ceil(sum(x_lists[ll]) / 262)) for ll in range(line_all)]) < 4:
            line_result = 3
    if line_result == 0 and len(detailed_lines) < 5:
        if sum([int(math.ceil(sum(x_lists[ll]) / 262)) for ll in range(line_all)]) < 5:
            line_result = 4
    if line_result == 0 and len(detailed_lines) < 6:
        if sum([int(math.ceil(sum(x_lists[ll]) / 343)) for ll in range(line_all)]) < 6:
            line_result = 5
    print(line_result)
    output = []
    line_now = 0
    for ii in range(line_all):
        input_line = ['', []]
        limit_now = line_limit[line_result][line_now]
        input_x = 0
        this_detailed_line = detailed_lines[ii]
        this_x_list = x_lists[ii]
        for jj in range(len(this_detailed_line[0])):
            if input_x + this_x_list[jj] > limit_now:
                if this_detailed_line[0][jj] in '，：；。！':
                    # 逆向处理
                    jj -= 1
                    input_x -= this_x_list[jj]
                    input_line[0] = input_line[0][:-1]
                    if jj in this_detailed_line[1]:
                        input_line[1].pop(jj)
                    # 强行换行
                    line_now += 1
                    limit_now = line_limit[line_result][line_now]
                    input_x = this_x_list[jj]
                    output.append(input_line)
                    input_line = [this_detailed_line[0][jj], []]
                    if jj in this_detailed_line[1]:
                        input_line[1].append(0)

                else:
                    line_now += 1
                    limit_now = line_limit[line_result][line_now]
                    input_x = this_x_list[jj]
                    output.append(input_line)
                    input_line = [this_detailed_line[0][jj], []]
                    if jj in this_detailed_line[1]:
                        input_line[1].append(0)
            else:
                input_x += this_x_list[jj]
                input_line[0] += this_detailed_line[0][jj]
                if jj in this_detailed_line[1]:
                    input_line[1].append(len(input_line[0]) - 1)
        line_now += 1
        output.append(input_line)
    
    print(output)
    print()
    return output


def z1(c='爱', s=36, f=font_1_34):
    _check = c.isascii()
    tx = _d_.textsize(c, f)
    if _check:
        w = tx[0] + 4
    else:
        w = s
    img = Image.new('RGBA', (w, s))
    d = ImageDraw.Draw(img)
    d.text((w // 2, s // 2), c, font=f, anchor='mm', fill='white', stroke_width=3, stroke_fill='black')
    # d.polygon([(0, 0), (0, s), (w, s), (w, 0)], outline='black')
    return img, w


def z2(c='爱', s=28, f=font_2_26):
    _check = c.isascii()
    tx = _d_.textsize(c, f)
    if _check:
        w = tx[0]
    else:
        w = s
    img = Image.new('RGBA', (w, s))
    d = ImageDraw.Draw(img)
    d.text((w // 2, s // 2), c, anchor='mm', font=f, fill='black')
    # d.text((w // 2, - int(round(s / 11))), c, anchor='ma', font=f, fill='black')
    # d.polygon([(0, 0), (0, s-1), (w-1, s-1), (w-1, 0)], outline='black')
    return img, w


def main():
    card = {
        'name': '高弗雷先辈',
        'text': '<b>战吼：</b>对所有其他随从造成2点伤害。如果有随从死亡，则重复此<b>战吼</b>效果。',
        'cardtype': 4,
        'rarity': 5,
        'clazz': [9],
        'dragon': True,
        'tag': False,
        'cost': 7,
        'atk': 4,
        'hp': 4,
        'flag': [0],
        'art_path': 'default.png',
    }
    hs_render(**card)


def test():
    # a = '测试，本1啊+2/+1！'
    # c_c = [z1(c) for c in a]
    # for cc in c_c:
    #     print(cc)
    aa = ['<b>突袭</b>，<b>超杀</b>：从你的牌库中抽一张法术牌。',
          '规则文本，十个字注意\n规则文本+2/+2字注意\n换行这里八个字了\n然后结束。',
          '<b>战吼：</b>对所有其他随从造成2点伤害。如果有随从死亡，则重复此<b>战吼</b>效果。'
          ]
    for a in aa:
        minion_break_lines(a, False)


if __name__ == "__main__":
    t0 = time.time()
    
    main()
    # test()
    
    print(time.time() - t0)
