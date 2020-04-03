import re
import string
from spellCorrection.preprocess.aug_dataset_v2 import *

vocabs_1 = []
with open("vocab/all-vietnamese-syllables.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        # line = norm_text(line)
        # line = remove_accent(line)
        vocabs_1.append(line)

vocabs_2 = []
with open("vocab/vn_remove_accent.txt", 'r') as rf:
    for line in rf.readlines():
        line = line.strip()
        # line = norm_text(line)
        # line = remove_accent(line)
        vocabs_2.append(line)

vocabs = vocabs_1 + vocabs_2


# def check_word_error_src(file_src, file_save_src):
#     text = text.strip()
#     texts = text.split(' ')
#     ls_txt = []
#     for txt in texts:
#         if txt.isalpha() and txt not in vocabs:
#             txt = list(txt)
#         ls_txt.append(txt)
#
#     return ' '.join(ls_txt)


if __name__ == '__main__':
    s = ' gfgf hôm nay tôi đais học 56 h '
    print(check_word_error(s))




