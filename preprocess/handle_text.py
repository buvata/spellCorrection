import re
import unidecode
import unicodedata
import string
import json

set_punctuations = set(string.punctuation)
list_punctuations_out = ['”', '”', "›", "“", '"']
for e_punc in list_punctuations_out:
    set_punctuations.add(e_punc)
print(set_punctuations)


def check_list_punct(text):
    for i in list(text):
        if i in set_punctuations:
            return False
        else:
            return True


def check_all_punct(txt):
    j = False
    for i in list(txt):
        if i in set_punctuations:
            j = True
        else:
            j = False
            break

    return j


def remove_accent(txt):
    return unidecode.unidecode(txt)


def norm_text(text):
    text = unicodedata.normalize('NFC', text)
    text = text.lower()
    text = re.sub(r"òa", "oà", text)
    text = re.sub(r"óa", "oá", text)
    text = re.sub(r"ỏa", "oả", text)
    text = re.sub(r"õa", "oã", text)
    text = re.sub(r"ọa", "oạ", text)
    text = re.sub(r"òe", "oè", text)
    text = re.sub(r"óe", "oé", text)
    text = re.sub(r"ỏe", "oẻ", text)
    text = re.sub(r"õe", "oẽ", text)
    text = re.sub(r"ọe", "oẹ", text)
    text = re.sub(r"ùy", "uỳ", text)
    text = re.sub(r"úy", "uý", text)
    text = re.sub(r"ủy", "uỷ", text)
    text = re.sub(r"ũy", "uỹ", text)
    text = re.sub(r"ụy", "uỵ", text)
    text = re.sub(r"Ủy", "Uỷ", text)
    return text


def remove_multi_space(text):
    text = text.replace("\n", " ")
    text = re.sub("\s\s+", " ", text)
    # handle exception when line just all of punctuation
    if len(text) == 0:
        return text
    if text[0] == " ":
        text = text[1:]
    if len(text) == 0:
        pass
    else:
        if text[-1] == " ":
            text = text[:-1]

    return "".join(text)


def handle_punctuation(text):
    l_new_char = []
    for e_char in text:
        if e_char not in list(set_punctuations):
            l_new_char.append(e_char)
        else:
            l_new_char.append(" {} ".format(e_char))

    text = "".join(l_new_char)

    return text


def link_punc(line):
    line = line.replace('_', '#')
    line = line.replace('\n', '')
    line = line.strip()
    l_txt = line.split(' ')
    current = ''
    for k, txt in enumerate(l_txt):
        new_word = ''
        if k == 0 and txt in set_punctuations:
            current += txt
        else:
            for i, t in enumerate(list(txt)):
                l_t = []
                if t in set_punctuations and i == len(list(txt))-1:
                    t = ' _' + t
                elif t in set_punctuations and 0 < i < len(list(txt))-1:
                    t = ' _' + t + ' '
                    (list(txt))[i+1] = ' _' + (list(txt))[i+1]
                    # print('a')
                elif t in set_punctuations and i == 0:
                    (list(txt))[i+1] = ' _' + (list(txt))[i+1]
                elif 0 < i < len(list(txt))-1 and list(txt)[i-1] in set_punctuations:
                    t = ' _' + t
                else:
                    t = t
                l_t.append(t)
                new_word += ''.join(l_t)

        current += ' ' + new_word

    current = remove_multi_space(current)

    current = current.split(' ')
    ls_txt = []
    for txt in current:
        if txt.replace('_', '').isalpha():
            txt = txt.replace("_", '')
        ls_txt.append(txt)

    return ' '.join(ls_txt)


def split_word(text):
    l = list(text)
    return '<oov> ' + ' _'.join(l) + ' </oov>'


def split_numeric(text):
    l = list(text)
    if l[0] == "_":
        return l[0] + ' _'.join(l[1:])
    return ' _'.join(l)


def find_word_tag(text):
    start_sep = '<oov>'
    end_sep = '</oov>'
    result = []
    tmp = text.split(start_sep)
    for par in tmp:
        if end_sep in par:
            t = par.split(end_sep)[0]
            result.append(t)
    return result


def check_index_in_vocab(vocab, index):
    keys = list(vocab.keys())
    values = list(vocab.values())
    for i, j in enumerate(keys):
        if index in values[i]:
            return i


def split_word_with_bound(text):
    txts = text.split(' ')
    ls_txt_oov = find_word_tag(text)

    list_index = {}
    i = 0
    j = 0
    while i < len(txts):
        if '<oov>' in txts[i]:
            if j in list(list_index.keys()):
                list_index[j].extend([i])
            if j not in list(list_index.keys()):
                list_index[j] = [i]

            while True:
                i += 1
                list_index[j].extend([i])
                if '</oov>' in txts[i]:
                    j += 1
                    break
        i += 1

    for i, ls in enumerate(ls_txt_oov):
        ls_txt_oov[i] = '<oov>' + ls + '</oov>'

    index_oov = []

    for i in range(len(list_index)):
        index_oov.extend(list_index[i])


    ls = []
    i = 0
    j = 0
    while i < len(txts):
        if i not in index_oov:
            ls.append(txts[i])
            j = 1
        else:
            index = check_index_in_vocab(list_index, i)
            word_oov = []
            for j in list_index[index]:
                word_oov.append(txts[j])
            ls.append(' '.join(word_oov))

            j = len(word_oov)
        i += j

    return ls


vocab_confusion_word = {}
with open("vocab/model_all-vietnamese-words-confusionset.txt") as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        key = line.split(':')[0]
        values = line.split(':')[1].split('|')
        vocab_confusion_word[key] = values

vocab_confusion_word_key = list(vocab_confusion_word.keys())
# vocab_confusion_word_value = list(vocab_confusion_word.values())
# print(vocab_confusion_word_key)

vocabs_vn_accent = []
with open("vocab/all-vietnamese-syllables.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        # line = remove_accent(line)
        vocabs_vn_accent.append(line)

vocabs_vn_non_accent = []
with open("vocab/vn_remove_accent.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        line = norm_text(line)
        # line = remove_accent(line)
        vocabs_vn_non_accent.append(line)

vocabs = set(vocabs_vn_accent + vocabs_vn_non_accent)


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


with open("vocab/keys_random.json", 'r') as rf:
    data_keys_random = json.load(rf)
ls_key_random = list(data_keys_random.keys())


with open("vocab/keys_last.json", 'r') as rf:
    data_keys_last = json.load(rf)
ls_keys_last = list(data_keys_last.keys())


def check_syll_vn(txt):
    if remove_accent(txt) != txt:
        if norm_text(txt) in vocabs_vn_accent:
            return True
        else:
            return False
    else:
        if txt in vocabs_vn_non_accent:
            return True
        else:
            return False


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


def format_output(text):
    text = norm_text(text)
    # text = link_punc(text)
    # text, _ = check_word_oov(text, text)

    text = text.replace('<oov>', '')
    text = text.replace('</oov>', '')
    text = remove_multi_space(text)

    texts = list(text)

    ls_txt = []
    for i, txt in enumerate(texts):

        if txt == ' ' and '_' in texts[i + 1]:
            txt = txt.replace(' ', '')

        txt = txt.replace('_', '')

        ls_txt.append(txt)

    lst = ''.join(ls_txt)

    return lst


def format_input(text):
    text = norm_text(text)
    text = text.replace("\n",'')
    text = remove_multi_space(text)
    ls_text = list(text)
    if ls_text[-1] != '.':
        ls_text.extend('.')
    text = ''.join(ls_text)

    text = link_punc(text)
    text_after_oov, _ = check_word_oov(text, text)

    return text_after_oov


if __name__ == '__main__':
    s = 'hôm nay toif di rất vui, gặp 37 bạn mới nhiễm covid-19 cách ly.'
    print(format_input(s))

