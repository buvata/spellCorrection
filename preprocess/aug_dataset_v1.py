import re
import numpy as np
import json
import random
#from underthesea import word_tokenize
from spellCorection.preprocess.handle_text import *
from tqdm import tqdm
import time

vocabs_1 = []
with open("vocab/all-vietnamese-syllables.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        # line = remove_accent(line)
        vocabs_1.append(line)

vocabs_2 = []
with open("vocab/vn_remove_accent.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        # line = remove_accent(line)
        vocabs_2.append(line)

vocabs = set(vocabs_1 + vocabs_2)

def check_syll_vn(txt):
    if norm_text(txt) in vocabs:
        return True
    else:
        return False


def random_remove_accent(text_src, text_des, thresh_hold=1):
    texts = split_word_with_bound(text_src)
    cnt = 0
    while True:
        i = np.random.randint(len(texts))
        cnt += 1
        if (check_syll_vn(texts[i]) and remove_accent(texts[i]) != texts[i]) or cnt == 3:
            break

    if cnt == 3:
        texts = texts

    else:
        prob = random.random()
        if prob < thresh_hold:
            texts[i] = remove_accent(texts[i])

    return ' '.join(texts), text_des


def change_accent(txt_src, txt_des, thresh_hold=1):
    ls_1 = ['ả', 'ẳ', 'ấ', 'ẻ', 'ể', 'ỏ', 'ổ', 'ở', 'ỉ', 'ỷ', 'ủ', 'ử']
    ls_2 = ['ã', 'ẵ', 'ẫ', 'ẽ', 'ễ', 'õ', 'ỗ', 'ỡ', 'ĩ', 'ỹ', 'ũ', 'ữ']

    texts = split_word_with_bound(txt_src)
    cnt = 0
    ls = random.sample(texts, len(texts))

    prob = random.random()
    if prob < thresh_hold:
        for txt in ls:
            if 'oov' not in txt:
                for i in txt:
                    if i in ls_1:
                        index = ls_1.index(i)
                        txt_src = txt_src.replace(i, ls_2[index])
                        cnt += 1
                        break

                    if i in ls_2:
                        index = ls_2.index(i)
                        txt_src = txt_src.replace(i, ls_1[index])
                        cnt += 1
                        break

            if cnt != 0:
                break

    return txt_src, txt_des


def random_del_word(txt_src, txt_des, thresh_hold=1):

    texts = split_word_with_bound(txt_src)
    cnt = 0
    while True:
        i = np.random.randint(len(texts))
        cnt += 1
        if ('<oov>' not in texts[i] and texts[i].isalpha()):
            prob = random.random()
            if prob < thresh_hold:
                texts.remove(texts[i])
            break
        if cnt == 3:
            texts = texts
            break

    return ' '.join(texts), txt_des


def change_first_char(text_src, text_des, index, thresh_hold=1):
    texts = split_word_with_bound(text_src)
    ls_text_des = split_word_with_bound(text_des)
    # index = texts.index(word)
    txt = texts[index]

    if txt.isalpha() and check_syll_vn(txt):
        prob = random.random()
        if prob < thresh_hold:
            if txt[0] == 's':
                txt = txt.replace(txt[0], 'x')
                # new_text.append(txt.replace(txt[0], 'x'))
            if txt[0] == 'x':
                txt = txt.replace(txt[0], 's')
                # new_text.append(txt.replace(txt[0], 's'))

            if txt[0] == 'r':
                txt = txt.replace(txt[0], 'd')
                # new_text.append(txt.replace(txt[0], 'd'))
            if txt[0] == 'd':
                txt = txt.replace(txt[0], 'r')
                # new_text.append(txt.replace(txt[0], 'r'))

            if txt[0] == 'n':
                txt = txt.replace(txt[0], 'l')
                # new_text.append(txt.replace(txt[0], 'l'))
            if txt[0] == 'l':
                txt = txt.replace(txt[0], 'n')
                # new_text.append(txt.replace(txt[0], 'n'))

            if txt[:2] == 'ch':
                txt = txt.replace(txt[:2], 'tr')
                # new_text.append(txt.replace(txt[:2], 'tr'))
            if txt[:2] == 'tr':
                txt = txt.replace(txt[:2], 'ch')
                # new_text.append(txt.replace(txt[:2], 'ch'))

        if check_syll_vn(txt):
            texts[index] = txt
        else:
            texts[index] = split_word(txt)
            ls_text_des[index] = split_word(txt)

    result = ' '.join(texts)

    return result, ' '.join(ls_text_des)


# def del_char_in_word(text_src, text_des, index, thresh_hold=1):
#     texts = split_word_with_bound(text_src)
#     ls_txt_des = split_word_with_bound(text_des)
#     # i = texts.index(word)
#     i = index
#     word = texts[i]
#
#     if word.isalpha() and check_syll_vn(word):
#         prob = random.random()
#         if prob < thresh_hold:
#             while True:
#                 j = np.random.randint(len(texts[i]))
#                 if texts[i][j].isalpha():
#                     texts[i] = texts[i][:j] + texts[i][j + 1:]
#                     texts[i] = split_word(texts[i])
#                     ls_txt_des[i] = split_word(ls_txt_des[i])
#                     break
#
#     return ' '.join(texts), ' '.join(ls_txt_des)


keys_break_typing = []
values_break_typing = []
with open("vocab/vn-break-typing.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        line = line.split(' ')
        keys_break_typing.append(line[0])
        values_break_typing.append(line[1])


vocabs_telex = {}
keys_wrong_telex = []
values_wrong_telex = []
with open("vocab/all-vietnamese-words-wrong-telex.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        line = line.split(' ')
        keys_wrong_telex.append(line[0])
        values_wrong_telex.append(line[1])

    for k, v in enumerate(keys_wrong_telex):
        try:
            vocabs_telex[v].append(values_wrong_telex[k])
        except KeyError:
            vocabs_telex[v] = [values_wrong_telex[k]]


def remove_split_word(txt_src, txt_des, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    cnt = 0

    while True:
        i = np.random.randint(len(texts)-1)
        cnt += 1
        if ('<oov>' not in texts[i] and '<oov>' not in texts[i+1] and check_list_punct(texts[i]) and check_list_punct(texts[i+1]))\
                or cnt == 3:
            break

    if cnt == 3:
        texts = texts
        ls_txt_des = ls_txt_des

    else:
        prob = random.random()
        if prob < thresh_hold:
            a = change_type_telex(texts[i], texts[i], 0, thresh_hold=1)[0].replace('</oov>', '')
            b = change_type_telex(texts[i + 1], texts[i + 1], 0, thresh_hold=1)[0].replace('<oov>', '')
            if a == texts[i] and b == texts[i+1]:
                texts[i] = texts[i] + texts[i+1]
                texts[i] = split_word(texts[i])

            elif a == texts[i]:
                a = split_word(a).replace('</oov>', '')
                b = '_' + remove_multi_space(b)
                texts[i] = a + b

            elif b == texts[i+1]:
                b = '_' + remove_multi_space(split_word(b).replace('<oov>', ''))
                texts[i] = a + b

            else:
                texts[i] = a + '_' + remove_multi_space(b)

            texts.remove(texts[i+1])

            ls_txt_des[i] = remove_multi_space(split_word(ls_txt_des[i]).replace('</oov>', '') + split_word(ls_txt_des[i+1]).replace('<oov>', ''))
            # ls_txt_des[i] = split_word(ls_txt_des[i])
            ls_txt_des.remove(ls_txt_des[i+1])

    return ' '.join(texts), ' '.join(ls_txt_des)



def add_char_in_last_word(txt_src, txt_des, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    cnt = 0

    while True:
        i = np.random.randint(len(texts))
        cnt += 1
        if ('<oov>' not in texts[i] and remove_accent(texts[i]) != texts[i]) or cnt == 3:
            break

    if cnt == 3:
        texts = texts
        ls_txt_des = ls_txt_des

    else:
        prob = random.random()
        if prob < thresh_hold:
            if check_syll_vn(texts[i]):
                if texts[i] in list(vocabs_telex.keys()):
                    ls_wr_txt = vocabs_telex[texts[i]]
                    texts[i] = split_word(random.choice(ls_wr_txt) + remove_accent(texts[i][-1]))
                    ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)



def change_type_telex(txt_src, txt_des, index, thresh_hold=1):
    ls_txt_des = split_word_with_bound(txt_des)
    texts = split_word_with_bound(txt_src)
    # i = texts.index(word)
    i = index

    if check_syll_vn(texts[i]):
        prob = random.random()
        if prob < thresh_hold:
            if texts[i] in list(vocabs_telex.keys()):
                ls_wr_txt = vocabs_telex[texts[i]]
                texts[i] = split_word(random.choice(ls_wr_txt))
                ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


def convert_typing_missing_char(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    if texts[i] != remove_accent(texts[i]) and check_syll_vn(texts[i]):
        prob = random.random()
        if prob < thresh_hold:
            texts[i] = texts[i][:-1]
            if check_syll_vn(texts[i]):
                texts[i] = texts[i]

            else:
                for k, v in enumerate(keys_break_typing):
                    if v in texts[i]:
                        texts[i] = texts[i].replace(v, values_break_typing[k])

                texts[i] = split_word(texts[i])
                ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


with open("vocab/keys_random.json", 'r') as rf:
    data_keys_random = json.load(rf)
ls_key_random = list(data_keys_random.keys())

def convert_random_word_distance_keyboard(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    if check_syll_vn(texts[i]):
        prob = random.random()
        if prob < thresh_hold:
            if texts[i][-1].isalpha() and remove_accent(texts[i][-1]) == texts[i][-1] and texts[i][-1] in ls_key_random:
                texts[i] = texts[i][:-1] + random.choice(data_keys_random[texts[i][-1]])
                if not check_syll_vn(texts[i]):
                    for k, v in enumerate(keys_break_typing):
                        if v in texts[i]:
                            texts[i] = texts[i].replace(v, values_break_typing[k])

                    texts[i] = split_word(texts[i])

                    ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


with open("vocab/keys_last.json", 'r') as rf:
    data_keys_last = json.load(rf)
ls_keys_last = list(data_keys_last.keys())


def convert_last_char_distance_keyboard(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    prob = random.random()
    if prob < thresh_hold:
        if check_syll_vn(texts[i]) and remove_accent(texts[i][-1]) == texts[i][-1] and texts[i][-1] in ls_keys_last:
            texts[i] = texts[i][:-1] + data_keys_last[texts[i][-1]][0]
            if not check_syll_vn(texts[i]):
                for k, v in enumerate(keys_break_typing):
                    if v in texts[i]:
                        texts[i] = texts[i].replace(v, values_break_typing[k])
                texts[i] = split_word(texts[i])
                ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


def convert_first_char_distance_keyboard(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    if check_syll_vn(texts[i]):
        prob = random.random()
        if prob < thresh_hold:
            if texts[i][-1].isalpha() and remove_accent(texts[i][0]) == texts[i][0] and texts[i][0] in ls_key_random:
                texts[i] = random.choice(data_keys_random[texts[i][0]]) + texts[i][1:]
                if not check_syll_vn(texts[i]):
                    for k, v in enumerate(keys_break_typing):
                        if v in texts[i]:
                            texts[i] = texts[i].replace(v, values_break_typing[k])

                    texts[i] = split_word(texts[i])

                    ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


def check_word_oov(txt_src, txt_des):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)

    for i, txt in enumerate(texts):
        if not check_syll_vn(txt) and check_list_punct(txt) and not txt.isnumeric():
            texts[i] = split_word(texts[i])
            ls_txt_des[i] = split_word(ls_txt_des[i])

        if txt.isnumeric():
            texts[i] = split_numeric(txt)
            ls_txt_des[i] = split_numeric(ls_txt_des[i])

        if not check_all_punct(txt) and not txt.isalnum():
            texts[i] = split_numeric(txt)
            ls_txt_des[i] = split_numeric(ls_txt_des[i])


    return ' '.join(texts), ' '.join(ls_txt_des)


def remove_accent_sent(text):
    texts = split_word_with_bound(text)
    for i, txt in enumerate(texts):
        if txt.isalpha() and '<oov>' not in txt:
            texts[i] = remove_accent(txt)

    return ' '.join(texts)


def augment_data(sent):

    ls = []

    sents = check_word_oov(sent, sent)[0]
    text_src, text_des = sents, sents

    prob = random.random()
    if prob < 0.2:
        prob = random.random()

        if prob < 0.3:
            text_src, text_des = random_remove_accent(sents, sents)
        if 0.3 < prob < 0.6:
            text_src, text_des = change_accent(sents, sents)
        if 0.6 < prob:
            text_src, text_des = remove_accent_sent(sents), sents

        ls.append('{}||{}'.format(text_src, text_des))

    elif 0.2 < prob < 0.4:
        n_augment_sent = 2

        prob = random.random()
        if prob < 0.3:
            n_augment_sent = 1

        for n_sent in range(n_augment_sent):
            text_src, text_des = sents, sents
            for index, word in enumerate(split_word_with_bound(text_src)):
                if word.isalpha() and '<oov>' not in word:
                    prob = random.random()
                    if prob < 0.15:
                        prob = random.random()

                        if prob < 0.25:
                            text_src, text_des = change_first_char(text_src, text_des, index)

                        if 0.25 < prob < 0.45:
                            text_src, text_des = change_type_telex(text_src, text_des, index)

                        if 0.45 < prob < 0.55:
                            text_src, text_des = convert_typing_missing_char(text_src, text_des, index)

                        if 0.55 < prob < 0.7:
                            text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)

                        if 0.7 < prob < 0.9:
                            text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)

                        if 0.9 < prob:
                            text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)
            ls.append('{}||{}'.format(text_src, text_des))

    elif 0.4 < prob < 0.5:
        prob = random.random()
        if prob < 0.3:
            text_src, text_des = random_remove_accent(sents, sents)
        if 0.3 < prob < 0.6:
            text_src, text_des = change_accent(sents, sents)
        if 0.6 < prob:
            text_src, text_des = random_remove_accent(sents, sents)
            text_src, text_des = change_accent(text_src, text_des)

        for index, word in enumerate(split_word_with_bound(text_src)):
            if word.isalpha() and '<oov>' not in word:
                prob = random.random()
                if prob < 0.15:
                    prob = random.random()

                    if prob < 0.15:
                        text_src, text_des = change_first_char(text_src, text_des, index)

                    if 0.15 < prob < 0.3:
                        text_src, text_des = change_type_telex(text_src, text_des, index)

                    if 0.3 < prob < 0.45:
                        text_src, text_des = convert_typing_missing_char(text_src, text_des, index)

                    if 0.45 < prob < 0.6:
                        text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)

                    if 0.6 < prob < 0.9:
                        text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)

                    if 0.9 < prob:
                        text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)

        ls.append('{}||{}'.format(text_src, text_des))

    elif 0.5 < prob < 0.7:
        text_src, text_des = sents, sents

        prob = random.random()
        if prob < 0.3:
            text_src, text_des = remove_split_word(sents, sents)

        if 0.3 < prob < 0.4:
            text_src, text_des = random_del_word(sents, sents)

        if 0.4 < prob < 0.5:
            text_src, text_des = random_remove_accent(sents, sents)
            text_src, text_des = random_del_word(text_src, text_des)

        if 0.5 < prob < 0.8:
            text_src, text_des = random_remove_accent(sents, sents)
            text_src, text_des = remove_split_word(text_src, text_des)

        if 0.8 < prob:
            text_src, text_src = add_char_in_last_word(sents, sents)

        if text_src != text_des:
            ls.append('{}||{}'.format(text_src, text_des))

    ls.append('{}||{}'.format(sents, sents))

    ls_text = list(set(ls))

    return ls_text


if __name__ == '__main__':
    # s = '<oov> hôm </oov> hỏi <oov> gấu <oov> <oov> ham </oov> <oov> miến </oov> <oov> trôi </oov> <oov> đi </oov> <oov> hoobc </oov>'
    s = 'Trong không họp báo hôm qua, <oov> who </oov> cho ăn biết bếu trong các ca đến nhiễm đến này, hơn "70% đã bình phục và xuất viện" '
    # print(link_punc(s))
    # print(random_remove_accent(s,s))
    # print(del_char_in_word(s,s, 'bếu'))
    # print(change_first_char(s, s, 'bếu'))
    # print(remove_split_word(s,s))
    # # print(add_char_in_word(s))
    # print(change_type_telex(s,s,1))

    print(convert_typing_missing_char(s, s, 1))
    print(convert_last_char_distance_keyboard(s,s,1))
    print(convert_random_word_distance_keyboard(s,s,1))
    print(convert_random_word_distance_keyboard(s,s,1))
    # start = time.time()
    # file_src = "data/train_data/sent_src.txt"
    # file_des = "data/train_data/sent_des.txt"
    # file_data = "data/train_data/demo-full.txt"
    # augment_data_1(file_data, file_src, file_des)
    # end = time.time() - start
    # print(end)
    # print(check_word_oov(s, s))
    # print(convert_first_char_distance_keyboard(s,s,'bếu'))
    # print(change_accent(s,s))
    # print(random_del_word(s,s))
    # print(add_char_in_last_word(s,s))


