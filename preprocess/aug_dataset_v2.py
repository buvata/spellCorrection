import numpy as np
import random
from spellCorrection.preprocess.handle_text import *


# def check_syll_vn(txt):
#     if norm_text(txt) in vocabs:
#         return True
#     else:
#         return False

# bỏ dấu 1 từ random
def random_remove_accent(text_src, text_des, index, thresh_hold=1):
    texts = split_word_with_bound(text_src)
    i = index
    if (check_syll_vn(texts[i]) and remove_accent(texts[i]) != texts[i]):
        prob = random.random()
        if prob < thresh_hold:
            texts[i] = remove_accent(texts[i])

    return ' '.join(texts), text_des


lst = [['ã', 'à', 'á', 'ạ'],
            ['ẵ', 'ă', 'ằ', 'ắ', 'ặ'],
            ['â', 'ẫ', 'ầ', 'ấ', 'ậ'],
            ['e', 'è', 'é', 'ẹ', 'ẽ'],
            ['ê', 'ề', 'ế', 'ệ', 'ễ'],
            ['ò', 'ó', 'ọ', 'õ'],
            ['ô', 'ồ', 'ố', 'ộ', 'ỗ'],
            ['ờ', 'ớ', 'ợ'],
            ['ì', 'í', 'ị'],
            ['ủ', 'ù', 'ú', 'ụ'],
            ['ừ', 'ứ', 'ự'],
            ['ỳ', 'ý', 'ỵ']]


vocabs_accent = {}
for ls in lst:
    for i in ls:
        list_pop = ls[:]
        list_pop.remove(i)
        vocabs_accent[i] = list_pop


# thay đổi dấu câu
def change_accent(txt_src, txt_des, thresh_hold=0.6):
    ls_1 = ['ả', 'ẳ', 'ấ', 'ẻ', 'ể', 'ỏ', 'ổ', 'ở', 'ỉ', 'ỷ', 'ủ', 'ử']
    ls_2 = ['ã', 'ẵ', 'ẫ', 'ẽ', 'ễ', 'õ', 'ỗ', 'ỡ', 'ĩ', 'ỹ', 'ũ', 'ữ']

    ls_3 = ['a', 'á', 'à', 'ã', 'ả', 'ạ', 'e', 'é', 'è', 'ẽ', 'ẻ', 'ẹ', 'o', 'ó', 'ò', 'õ', 'ỏ', 'ọ']
    ls_4 = ['â', 'ấ', 'ầ', 'ẫ', 'ẩ', 'ậ', 'ê', 'ế', 'ề', 'ễ', 'ể', 'ệ', 'ô', 'ố', 'ồ', 'ỗ', 'ổ', 'ộ']

    list_vowel = ['o', 'e', 'i', 'u', 'a', 'ê']

    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)

    cnt = 0
    # ls = random.sample(texts, len(texts))

    prob = random.random()
    # đổi dấu hỏi , ngã
    # if prob < 0.4:
    #     print('1.1')
    #     for k, txt in enumerate(texts):
    #         if txt.isalpha() and 'oov' not in str(txt):
    #             for e, i in enumerate(txt):
    #                 if i in ls_1:
    #                     index = ls_1.index(i)
    #                     texts[k] = texts[k].replace(i, ls_2[index])
    #                     cnt += 1
    #                     break
    #
    #                 if i in ls_2:
    #                     index = ls_2.index(i)
    #                     texts[k] = texts[k].replace(i, ls_1[index])
    #                     cnt += 1
    #                     break
    #
    #             if texts[k] in vocabs_vn_accent:
    #                 texts[k] = texts[k]
    #             else:
    #                 for j, v in enumerate(keys_break_typing):
    #                     if v in texts[k]:
    #                         texts[k] = texts[k].replace(v, values_break_typing[j])
    #
    #                 texts[k] = split_word(texts[k])
    #                 ls_txt_des[k] = split_word(ls_txt_des[k])
    #
    #         if cnt != 0:
    #             break

    list_sent_src = []
    list_sent_des = []

    if  prob < 1:
        # print('1.2')
        while True:
            i = np.random.randint(len(texts))
            cnt += 1

            if (texts[i].isalpha() and '<oov>' not in texts[i]):
                a = texts[i]
                if remove_accent(texts[i]) in vocab_confusion_word_key:
                    list_word_choice = vocab_confusion_word[remove_accent(texts[i])]

                    for word_change in list_word_choice:
                        if not check_syll_vn(word_change):
                            texts[i] = split_word(word_change)
                            ls_txt_des[i] = split_word(a)

                        else:
                            texts[i] = word_change
                            ls_txt_des[i] = a

                        list_sent_src.append(' '.join(texts))
                        list_sent_des.append(' '.join(ls_txt_des))
                break

            if cnt == 3:
                texts = texts

                list_sent_src.append(' '.join(texts))
                list_sent_des.append(' '.join(ls_txt_des))
                break

    # đổi à -> á, ạ,  é -> è, ẹ
    # elif 0.5 < prob < 0.8:
    #     for k,txt in enumerate(texts):
    #         if txt.isalpha() and 'oov' not in str(txt):
    #             for i in txt:
    #                 if i in list(vocabs_accent.keys()):
    #                     texts[k] = texts[k].replace(i, random.choice(vocabs_accent[i]))
    #                     cnt += 1
    #                     break
    #
    #             if texts[k] in vocabs_vn_accent:
    #                 texts[k] = texts[k]
    #             else:
    #                 for j, v in enumerate(keys_break_typing):
    #                     if v in texts[k]:
    #                         texts[k] = texts[k].replace(v, values_break_typing[j])
    #
    #                 texts[k] = split_word(texts[k])
    #                 ls_txt_des[k] = split_word(ls_txt_des[k])
    #
    #         if cnt != 0:
    #             break

    # đổi a -> â , e -> ê
    # elif 0.8 < prob:
    #     print('1.3')
    #     for k, txt in enumerate(texts):
    #         if txt.isalpha() and 'oov' not in str(txt):
    #             for e, i in enumerate(txt):
    #                 if i in ls_3:
    #                     if e < len(txt) - 1:
    #                         if txt[e+1] not in list_vowel:
    #                             index = ls_3.index(i)
    #                             texts[k] = texts[k].replace(i, ls_4[index])
    #                             cnt += 1
    #                             break
    #                     else:
    #                         index = ls_3.index(i)
    #                         texts[k] = texts[k].replace(i, ls_4[index])
    #                         cnt += 1
    #                         break
    #
    #                 if i in ls_4:
    #                     if e < len(txt) - 1:
    #                         if txt[e+1] not in list_vowel:
    #                             index = ls_4.index(i)
    #                             texts[k] = texts[k].replace(i, ls_3[index])
    #                             cnt += 1
    #                             break
    #                     else:
    #                         index = ls_4.index(i)
    #                         texts[k] = texts[k].replace(i, ls_3[index])
    #                         cnt += 1
    #                         break
    #
    #             if check_syll_vn(texts[k]):
    #                 texts[k] = texts[k]
    #             else:
    #                 prob = random.random()
    #                 if prob < 0.6:
    #                     for j, v in enumerate(keys_break_typing):
    #                         if v in texts[k]:
    #                             texts[k] = texts[k].replace(v, values_break_typing[j])
    #
    #                     texts[k] = split_word(texts[k])
    #                     ls_txt_des[k] = split_word(ls_txt_des[k])
    #
    #                 else:
    #                     texts[k] = split_word(texts[k])
    #                     ls_txt_des[k] = split_word(ls_txt_des[k])
    #
    #         if cnt != 0:
    #             break


    return list_sent_src, list_sent_des

# xóa 1 từ bất kì nằm trong vocab
def random_del_word(txt_src, txt_des, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    cnt = 0

    while True:
        i = np.random.randint(len(texts))
        cnt += 1
        if (texts[i].isalpha() and '<oov>' not in str(texts[i])):
            prob = random.random()
            if prob < thresh_hold:
                texts.remove(texts[i])
            break

        if cnt == 2:
            texts = texts
            break

    return ' '.join(texts), txt_des

# thêm 1 từ bất kì trong vocab
def random_add_word(txt_src, txt_des, thresh_hold=1):
    texts = split_word_with_bound(txt_src)

    prob = random.random()
    if prob < thresh_hold:
        index = np.random.randint(len(texts))
        word_random = random.choice(vocabs_vn_accent[32:])
        texts.insert(index, word_random)

    return ' '.join(texts), txt_des

# thay đổi chữ đầu : n->l , s->x ,...
def change_first_char(text_src, text_des, thresh_hold=1):
    texts = split_word_with_bound(text_src)
    ls_text_des = split_word_with_bound(text_des)
    ls_char_1 = ['x', 's', 'r', 'd', 'n', 'l']
    ls_char_2 = ['ch', 'tr', 'gi']
    cnt = 0

    while True:
        i = np.random.randint(len(texts))
        cnt += 1
        if ('<oov>' not in str(texts[i]) and (texts[i][0] in ls_char_1 or texts[i][:2] in ls_char_2)) or cnt == 5:
            break

    if cnt == 5:
        texts = texts
    else:
        if check_syll_vn(texts[i]):
            prob = random.random()
            txt = list(texts[i])
            if prob < thresh_hold:

                if txt[0] == 's':
                    txt[0] = 'x'
                    txt = ''.join(txt)
                elif txt[0] == 'x':
                    txt[0] = 's'
                    txt = ''.join(txt)

                elif txt[0] == 'r':
                    txt[0] = 'd'
                    txt = ''.join(txt)
                elif txt[0] == 'd':
                    prob = random.random()
                    if prob < 0.5:
                        txt[0] = 'r'
                        txt = ''.join(txt)
                    else:
                        txt[0] = 'gi'
                        txt = ''.join(txt)

                elif ''.join(txt[:2]) == 'gi':
                    txt[0] = 'd'
                    txt[1] = ''
                    txt = ''.join(txt)

                elif txt[0] == 'n':
                    txt[0] = 'l'
                    txt = ''.join(txt)

                elif txt[0] == 'l':
                    txt[0] = 'n'
                    txt = ''.join(txt)

                elif ''.join(txt[:2]) == 'ch':
                    txt[0] = 't'
                    txt[1] = 'r'
                    txt = ''.join(txt)

                elif ''.join(txt[:2]) == 'tr':
                    txt[0] = 'c'
                    txt[1] = 'h'
                    txt = ''.join(txt)

            if check_syll_vn(txt):
                texts[i] = txt
            else:
                texts[i] = split_word(txt)
                ls_text_des[i] = split_word(ls_text_des[i])

    result = ' '.join(texts)

    return result, ' '.join(ls_text_des)

# đổi các kí tự trong 1 từ : hôm -> hoom -> hmoo, nay -> nya
def random_swap_char_in_word(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)

    prob = random.random()
    if prob < thresh_hold:
        if check_syll_vn(texts[index]) and len(texts[index]) > 2:
            texts[index], _ = change_type_telex(texts[index], texts[index], 0)
            texts[index] = texts[index].replace('<oov>', '')
            texts[index] = texts[index].replace('</oov>', '')
            texts[index] = texts[index].replace('_', '')
            texts[index] = texts[index].replace(' ', '')

            i = np.random.randint(1, len(texts[index])-1)
            j = np.random.randint(1, len(texts[index])-1)

            ls_texts = list(texts[index])
            ls_texts[i], ls_texts[j] = ls_texts[j], ls_texts[i]

            if check_syll_vn(''.join(ls_texts)):
                texts[index] = ''.join(ls_texts)
                ls_txt_des[index] = ls_txt_des[index]
            else:
                texts[index] = split_word(''.join(ls_texts))
                ls_txt_des[index] = split_word(ls_txt_des[index])

    return ' '.join(texts), ' '.join(ls_txt_des)

# thay thế 1 từ bất kì và vỡ telex với xác suất: vui -> với -> vowis || vui -> với
def random_change_word_and_break(txt_src, txt_des, index, thresh_hold=0.4):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)

    prob = random.random()
    if prob < thresh_hold:
        if (texts[index] in vocabs_vn_accent):
            index_random = np.random.randint(len(vocabs_vn_accent))
            texts[index] = vocabs_vn_accent[index_random]
            texts[index], _ = change_type_telex(texts[index], texts[index], 0)

            if 'oov' in texts[index]:
                ls_txt_des[index] = split_word(ls_txt_des[index])

    else:
        if (texts[index] in vocabs_vn_accent):
            index_random = np.random.randint(len(vocabs_vn_accent))
            texts[index] = vocabs_vn_accent[index_random]

    return ' '.join(texts), ' '.join(ls_txt_des)


def random_change_word_simmilar_and_break(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)

    prob = random.random()
    if prob < thresh_hold:
        if (texts[index] in vocabs_vn_accent):
            index_random = vocabs_vn_accent.index(texts[index])
            if index_random > 5:
                texts[index] = random.choice(vocabs_vn_accent[index_random-5:index_random+5])
            else:
                texts[index] = random.choice(vocabs_vn_accent[index_random:index_random+5])

            texts[index], _ = change_type_telex(texts[index], texts[index], 0)

            if 'oov' in texts[index]:
                ls_txt_des[index] = split_word(ls_txt_des[index])

    return ' '.join(texts), ' '.join(ls_txt_des)

# bỏ space giữa 2 từ: anh chị -> anhchij || anh chị -> anhchị
def remove_split_word(txt_src, txt_des, thresh_hold=0.4):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)

    cnt = 0
    while True:
        i = np.random.randint(len(texts)-1)
        cnt += 1
        if ('<oov>' not in str(texts[i]) and '<oov>' not in str(texts[i+1]) and check_list_punct(texts[i]) and check_list_punct(texts[i+1]))\
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

            ls_txt_des[i] = remove_multi_space(split_word(ls_txt_des[i]).replace('</oov>', '') + split_word(ls_txt_des[i+1]).replace('<oov>', ''))
            # ls_txt_des[i] = split_word(ls_txt_des[i])

        else:
            texts[i] = split_word(texts[i] + texts[i+1])
            ls_txt_des[i] = split_word(ls_txt_des[i]).replace('</oov>', '') + split_word(ls_txt_des[i+1]).replace('<oov>', '')
            ls_txt_des[i] = remove_multi_space(ls_txt_des[i])

        texts.remove(texts[i + 1])
        ls_txt_des.remove(ls_txt_des[i + 1])

    return ' '.join(texts), ' '.join(ls_txt_des)

# thêm kí tự vào đầu hoặc cuối từ: nay -> nnay || nay -> nayy
def add_char_in_word(txt_src, txt_des, index, thresh_hold=0.5):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    i = index

    prob = random.random()
    if prob < thresh_hold:
        if check_syll_vn(texts[i]):
            prob = random.random()
            if prob < 0.7:
                if texts[i] in list(vocabs_telex.keys()):
                    ls_wr_txt = vocabs_telex[texts[i]]
                    texts[i] = split_word(random.choice(ls_wr_txt) + remove_accent(texts[i][-1]))
                    ls_txt_des[i] = split_word(ls_txt_des[i])

            else:
                texts[i] = split_word(texts[i] + texts[i][-1])
                ls_txt_des[i] = split_word(ls_txt_des[i])

    else:
        if check_syll_vn(texts[i]):
            prob = random.random()
            if prob < 0.7:
                if texts[i] in list(vocabs_telex.keys()):
                    ls_wr_txt = vocabs_telex[texts[i]]
                    texts[i] = split_word(remove_accent(texts[i][0]) + random.choice(ls_wr_txt))
                    ls_txt_des[i] = split_word(ls_txt_des[i])
            else:
                # không vỡ telex : hôm -> hhôm
                texts[i] = split_word(remove_accent(texts[i][0]) + texts[i])
                ls_txt_des[i] = split_word(ls_txt_des[i])


    return ' '.join(texts), ' '.join(ls_txt_des)

# lỗi telex: hôm -> hoom
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

# mất kí tự cuối hoặc bất kì: nay -> na
def convert_typing_missing_char(txt_src, txt_des, index, thresh_hold=0.7):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    if check_syll_vn(texts[i]) and len(texts[i]) > 1:
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

        else:
            j = np.random.randint(len(texts[i]))
            texts[i] = texts[i][:j] + texts[i][j+1:]
            if check_syll_vn(texts[i]):
                texts[i] = texts[i]
            else:
                for k, v in enumerate(keys_break_typing):
                    if v in texts[i]:
                        texts[i] = texts[i].replace(v, values_break_typing[k])

                texts[i] = split_word(texts[i])
                ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)

# thay kí tự cuối hoặc bất kì bằng phím gần
def convert_random_word_distance_keyboard(txt_src, txt_des, index, thresh_hold=0.6):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    i = index

    if check_syll_vn(texts[i]):
        prob = random.random()
        if prob < thresh_hold:
            if texts[i][-1] in ls_key_random:
                texts[i] = texts[i][:-1] + random.choice(data_keys_random[texts[i][-1]])
                if not check_syll_vn(texts[i]):
                    for k, v in enumerate(keys_break_typing):
                        if v in texts[i]:
                            texts[i] = texts[i].replace(v, values_break_typing[k])

                    texts[i] = split_word(texts[i])
                    ls_txt_des[i] = split_word(ls_txt_des[i])

        else:
            j = np.random.randint(len(texts[i]))
            if texts[i][j] in ls_key_random:
                texts[i] = texts[i][:j] + random.choice(data_keys_random[texts[i][j]]) + texts[i][j + 1:]
                if not check_syll_vn(texts[i]):
                    for k, v in enumerate(keys_break_typing):
                        if v in texts[i]:
                            texts[i] = texts[i].replace(v, values_break_typing[k])

                    texts[i] = split_word(texts[i])
                    ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


def convert_last_char_distance_keyboard(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    prob = random.random()
    if prob < thresh_hold:
        if check_syll_vn(texts[i]) and len(texts[i]) > 1 and texts[i][-1] in ls_keys_last:
            texts[i] = texts[i][:-1] + data_keys_last[texts[i][-1]][0]
            if not check_syll_vn(texts[i]):
                prob = random.random()
                if prob < 0.8:
                    for k, v in enumerate(keys_break_typing):
                        if v in texts[i]:
                            texts[i] = texts[i].replace(v, values_break_typing[k])
                    texts[i] = split_word(texts[i])
                    ls_txt_des[i] = split_word(ls_txt_des[i])

                else:
                    texts[i] = split_word(texts[i])
                    ls_txt_des[i] = split_word(ls_txt_des[i])

    return ' '.join(texts), ' '.join(ls_txt_des)


def convert_first_char_distance_keyboard(txt_src, txt_des, index, thresh_hold=1):
    texts = split_word_with_bound(txt_src)
    ls_txt_des = split_word_with_bound(txt_des)
    # i = texts.index(word)
    i = index

    if check_syll_vn(texts[i]) and len(texts[i]) > 1:
        prob = random.random()
        if prob < thresh_hold:
            if texts[i][0] in ls_key_random:
                texts[i] = random.choice(data_keys_random[texts[i][0]]) + texts[i][1:]
                if not check_syll_vn(texts[i]):
                    prob = random.random()
                    if prob < 0.7:
                        for k, v in enumerate(keys_break_typing):
                            if v in texts[i]:
                                texts[i] = texts[i].replace(v, values_break_typing[k])

                        texts[i] = split_word(texts[i])
                        ls_txt_des[i] = split_word(ls_txt_des[i])

                    else:
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
        if txt.isalpha() and '<oov>' not in str(txt):
            texts[i] = remove_accent(txt)

    return ' '.join(texts)


def augment_data(sent):

    ls = []
    # trace_code = []
    sents_after_oov = check_word_oov(sent, sent)[0]

    text_src, text_des = sents_after_oov, sents_after_oov

    n_augment_sent = 1
    prob = random.random()
    if prob < 0.7:
        # trace_code.append("1")
        if len(text_src) > 25:
            # trace_code.append("1.1")
            n_augment_sent = random.choice([2, 3])
        elif 15 < len(split_word_with_bound(text_src)) <= 25:
            # trace_code.append("1.2")
            n_augment_sent = random.choice([1, 2])

    prob = random.random()
    if prob < 0.4:
        # trace_code.append("2")
        text_src, text_des = remove_accent(sents_after_oov), sents_after_oov
        ls.append('{}||{}'.format(text_src, text_des))


    for n_sent in range(n_augment_sent):

        if prob < 0.2:
            # trace_code.append("2")
            text_src, text_des = sents_after_oov, sents_after_oov
            for index, word in enumerate(split_word_with_bound(text_src)):
                if word.isalpha() and '<oov>' not in str(word):
                    # trace_code.append(2.1)
                    prob = random.random()
                    if prob < 0.15:
                        # trace_code.append("2.2")
                        prob = random.random()

                        if prob < 0.2:
                            # trace_code.append("2.2.1")
                            text_src, text_des = change_type_telex(text_src, text_des, index)

                        if 0.2 < prob < 0.25:
                            # trace_code.append("2.2.2")
                            text_src, text_des = random_change_word_and_break(text_src, text_des, index)

                        if 0.25 < prob < 0.4:
                            # trace_code.append("2.2.3")
                            text_src, text_des = convert_typing_missing_char(text_src, text_des, index)

                        if 0.4 < prob < 0.55:
                            # trace_code.append("2.2.4")
                            text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)

                        if 0.55 < prob < 0.65:
                            # trace_code.append("2.2.5")
                            text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)

                        if 0.65 < prob < 0.8:
                            # trace_code.append("2.2.6")
                            text_src, text_des = random_swap_char_in_word(text_src, text_des, index)

                        if 0.8 < prob < 0.9:
                            # trace_code.append("2.2.7")
                            text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)

                        if 0.9 < prob:
                            # trace_code.append("2.2.8")
                            text_src, text_des = add_char_in_word(text_src, text_des, index)

            prob = random.random()
            if prob < 0.5:
                # trace_code.append("2.3")
                text_src, text_des = random_add_word(text_src, text_des)

            # if check_oov_by_line(text_src, text_des):
            #     print(# trace_code)
            # text_src = remove_accent(text_src)
            ls.append('{}||{}'.format(text_src, text_des))


        elif 0.2 < prob < 0.35:
            # trace_code.append("3")
            text_src, text_des = sents_after_oov, sents_after_oov

            prob = random.random()
            if prob < 0.4:
                # trace_code.append("3.1")
                text_src, text_des = remove_split_word(text_src, text_des)

            for index, word in enumerate(split_word_with_bound(text_src)):
                if word.isalpha() and '<oov>' not in str(word):
                    # trace_code.append("3.2")
                    prob = random.random()

                    if prob < 0.1:
                        # trace_code.append("3.3")
                        prob = random.random()

                        if prob < 0.1:
                            # trace_code.append("3.3.1")
                            text_src, text_des = random_remove_accent(text_src, text_des, index)

                        if 0.1 < prob < 0.15:
                            # trace_code.append("3.3.2")
                            text_src, text_des = random_change_word_and_break(text_src, text_des, index)

                        if 0.15 < prob < 0.3:
                            # trace_code.append("3.3.3")
                            text_src, text_des = change_type_telex(text_src, text_des, index)

                        if 0.3 < prob < 0.4:
                            # trace_code.append("3.3.4")
                            text_src, text_des = convert_typing_missing_char(text_src, text_des, index)

                        if 0.4 < prob < 0.55:
                            # trace_code.append("3.3.5")
                            text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)

                        if 0.55 < prob < 0.65:
                            # trace_code.append("3.3.6")
                            text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)

                        if 0.65 < prob < 0.75:
                            # trace_code.append("3.3.7")
                            text_src, text_des = random_swap_char_in_word(text_src, text_des, index)

                        if 0.75 < prob < 0.85:
                            # trace_code.append("3.3.8")
                            text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)

                        if 0.85 < prob:
                            # trace_code.append("3.3.9")
                            text_src, text_des = add_char_in_word(text_src, text_des, index)

            prob = random.random()
            if prob < 0.5:
                # trace_code.append("3.4")
                text_src, text_des = random_del_word(text_src, text_des)

            # if check_oov_by_line(text_src, text_des):
            #     print(# trace_code)
            # text_src = remove_accent(text_src)
            ls.append('{}||{}'.format(text_src, text_des))

        elif 0.35 < prob < 0.5:
            # trace_code.append("4")
            text_src, text_des = sents_after_oov, sents_after_oov

            for index, word in enumerate(split_word_with_bound(text_src)):
                if word.isalpha() and '<oov>' not in str(word):
                    prob = random.random()
                    # trace_code.append("4.1")

                    if prob < 0.1:
                        # trace_code.append("4.2")
                        prob = random.random()

                        if prob < 0.1:
                            # trace_code.append("4.2.1")
                            text_src, text_des = random_remove_accent(text_src, text_des, index)

                        if 0.1 < prob < 0.15:
                            # trace_code.append("4.2.2")
                            text_src, text_des = random_change_word_and_break(text_src, text_des, index)

                        if 0.15 < prob < 0.3:
                            # trace_code.append("4.2.3")
                            text_src, text_des = change_type_telex(text_src, text_des, index)

                        if 0.3 < prob < 0.45:
                            # trace_code.append("4.2.4")
                            text_src, text_des = convert_typing_missing_char(text_src, text_des, index)

                        if 0.45 < prob < 0.55:
                            # trace_code.append("4.2.5")
                            text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)

                        if 0.55 < prob < 0.65:
                            # trace_code.append("4.2.6")
                            text_src, text_des = random_swap_char_in_word(text_src, text_des, index)

                        if 0.65 < prob < 0.75:
                            # trace_code.append("4.2.7")
                            text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)

                        if 0.75 < prob < 0.85:
                            # trace_code.append("4.2.8")
                            text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)

                        if 0.85 < prob:
                            # trace_code.append("4.2.9")
                            text_src, text_des = add_char_in_word(text_src, text_des, index)

            prob = random.random()
            if prob < 0.5:
            #     # trace_code.append("4.3")
                list_text_src, list_text_des = change_accent(text_src, text_des)
                for i, text_src in enumerate(list_text_src):
                    ls.append('{}||{}'.format(text_src, list_text_des[i]))

            if 0.5 < prob < 0.8:
                # trace_code.append("4.4")
                text_src, text_des = change_first_char(text_src, text_des)
            # if check_oov_by_line(text_src, text_des):
            #     print(# trace_code)
            # text_src = remove_accent(text_src)
                ls.append('{}||{}'.format(text_src, text_des))

            if 0.8 < prob:
                ls.append('{}||{}'.format(text_src, text_des))


        elif 0.5 < prob < 0.6:
            # trace_code.append("5")
            text_src, text_des = sents_after_oov, sents_after_oov

            prob = random.random()
            if prob < 0.2:
                # trace_code.append("5.1")
                text_src, text_des = remove_split_word(sents_after_oov, sents_after_oov)
                list_text_src, list_text_des = change_accent(text_src, text_des)
                for i, text_src in enumerate(list_text_src):
                    ls.append('{}||{}'.format(text_src, list_text_des[i]))
                # text_src, text_des = random_remove_accent(text_src, text_des)


            if 0.2 < prob < 0.45:
                # trace_code.append("5.2")
                text_src, text_des = change_first_char(sents_after_oov, sents_after_oov)
                text_src, text_des = random_del_word(text_src, text_des)
                ls.append('{}||{}'.format(text_src, text_des))

            if 0.45 < prob < 0.65:
                # trace_code.append("5.3")
                # text_src, text_des = change_accent(sents_after_oov, sents_after_oov)
                text_src, text_des = random_del_word(text_src, text_des)
                ls.append('{}||{}'.format(text_src, text_des))

            if 0.65 < prob < 0.8:
                # trace_code.append("5.4")
                text_src, text_des = remove_split_word(sents_after_oov, sents_after_oov)
                text_src, text_des = change_first_char(text_src, text_des)
                ls.append('{}||{}'.format(text_src, text_des))

            if 0.8 < prob:
                # trace_code.append("5.5")
                text_src, text_des = random_add_word(text_src, text_des)
            # if check_oov_by_line(text_src, text_des):
            #     print(# trace_code)
            # text_src = remove_accent(text_src)
                ls.append('{}||{}'.format(text_src, text_des))


        elif 0.6 < prob < 0.7:
            # trace_code.append("6")
            text_src, text_des = sents_after_oov, sents_after_oov

            prob = random.random()
            if prob < 0.2:
                # trace_code.append("6.1")
                text_src, text_des = remove_split_word(text_src, text_des)

            for index, word in enumerate(split_word_with_bound(text_src)):
                if word.isalpha() and '<oov>' not in str(word):
                    prob = random.random()
                    # trace_code.append("6.2")
                    if prob < 0.1:
                        prob = random.random()
                        # trace_code.append("6.3")

                        if prob < 0.1:
                            # trace_code.append("6.3.1")
                            text_src, text_des = random_remove_accent(text_src, text_des, index)

                        if 0.1 < prob < 0.2:
                            # trace_code.append("4.2.2")
                            text_src, text_des = random_change_word_and_break(text_src, text_des, index)

                        if 0.2 < prob < 0.35:
                            # trace_code.append("6.3.2")
                            text_src, text_des = change_type_telex(text_src, text_des, index)

                        if 0.35 < prob < 0.45:
                            # trace_code.append("6.3.3")
                            text_src, text_des = convert_typing_missing_char(text_src, text_des, index)

                        if 0.45 < prob < 0.55:
                            # trace_code.append("6.3.4")
                            text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)

                        if 0.55 < prob < 0.65:
                            # trace_code.append("6.3.5")
                            text_src, text_des = random_swap_char_in_word(text_src, text_des, index)

                        if 0.65 < prob < 0.75:
                            # trace_code.append("6.3.6")
                            text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)

                        if 0.75 < prob < 0.85:
                            # trace_code.append("6.3.7")
                            text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)

                        if 0.85 < prob:
                            # trace_code.append("6.3.8")
                            text_src, text_des = add_char_in_word(text_src, text_des, index)

            prob = random.random()
            if prob < 0.3:
                # trace_code.append("7")
                text_src, text_des = change_first_char(text_src, text_des)
                ls.append('{}||{}'.format(text_src, text_des))

            elif 0.3 < prob < 0.6:
               # trace_code.append("8")
               list_text_src, list_text_des = change_accent(text_src, text_des)
               for i, text_src in enumerate(list_text_src):
                   ls.append('{}||{}'.format(text_src, list_text_des[i]))

            elif 0.6 < prob:
                # trace_code.append("9")
                text_src, text_des = random_del_word(text_src, text_des)
            # if check_oov_by_line(text_src, text_des):
            #     print(# trace_code)
            # text_src = remove_accent(text_src)
                ls.append('{}||{}'.format(text_src, text_des))

    # if check_oov_by_line(text_src, text_des):
    #     print(# trace_code)
    ls.append('{}||{}'.format(sents_after_oov, sents_after_oov))

    ls_text = list(set(ls))

    return ls_text


def augment_data_extra(sent):
    ls = []

    # trace_code = []
    sents_after_oov = check_word_oov(sent, sent)[0]

    prob = random.random()
    if prob < 0.2:
        # print('1')
        ls = augment_data(sent)

    elif 0.2 < prob < 0.35:
        # print('2')
        text_src, text_des = sents_after_oov, sents_after_oov
        index = np.random.randint(len(split_word_with_bound(text_src)))
        text_src, text_des = random_change_word_and_break(text_src, text_des, index)
        ls.append('{}||{}'.format(text_src, text_des))

    elif 0.45 < prob < 0.6:
        # print('3')
        text_src, text_des = sents_after_oov, sents_after_oov
        index = np.random.randint(len(split_word_with_bound(text_src)))
        text_src, text_des = random_change_word_simmilar_and_break(text_src, text_des, index)
        ls.append('{}||{}'.format(text_src, text_des))

    elif 0.6 < prob < 0.8:
        # print('4')
        text_src, text_des = sents_after_oov, sents_after_oov
        text_src, text_des = random_add_word(text_src, text_des)
        ls.append('{}||{}'.format(text_src, text_des))

    elif 0.8 < prob:
        # print('5')
        text_src, text_des = sents_after_oov, sents_after_oov
        text_src, text_des = random_del_word(text_src, text_des)
        ls.append('{}||{}'.format(text_src, text_des))


    return ls




if __name__ == '__main__':
    # s = '<oov> hôm </oov> hỏi <oov> gấu <oov> <oov> ham </oov> <oov> miến </oov> <oov> trôi </oov> <oov> đi </oov> <oov> hoobc </oov>'
#    s = "bà trình bày với toà rằng không hứa hẹn gì với ông t. hết: tôi thấy vợ chồng nó nghèo khổ kêu về cho ở nhờ, tôi còn cho mượn một chỉ vàng và một ngàn đồng bạc để có vốn làm ăn."
    s = ' vào thời đó, người đẹp bị nghi đã sửa mũi và nâng cung mắt.'

    text_src = link_punc(s)
    text_des = text_src
    text_src, text_des = check_word_oov(text_src, text_des)
    print(change_accent(text_src, text_des))
    # print(remove_split_word(text_src,text_des))
    # print(augment_data_extra(text_src))
    # index = 1

    # text_src, text_des = random_remove_accent(text_src, text_des, index)
    # print(text_src, text_des)


    # text_src, text_des = random_change_word_and_break(text_src, text_des, index)
    # print(text_src, text_des)
    # text_src, text_des = random_change_word_simmilar_and_break(text_src, text_des, index)
    # text_src, text_des = change_type_telex(text_src, text_des, index)
    # print(text_src, text_des)

    # text_src, text_des = convert_typing_missing_char(text_src, text_des, index)
    # print(text_src, text_des)

    # text_src, text_des = convert_random_word_distance_keyboard(text_src, text_des, index)
    # print(text_src, text_des)

    # text_src, text_des = random_swap_char_in_word(text_src, text_des, index)
    # print(text_src, text_des)

    # text_src, text_des = convert_last_char_distance_keyboard(text_src, text_des, index)
    # print(text_src, text_des)

    # text_src, text_des = convert_first_char_distance_keyboard(text_src, text_des, index)
    #
    #
    # text_src, text_des = add_char_in_word(text_src, text_des, index)

