import os
# a = os.system('')

def cut_line(folder):
    list_file_a = os.listdir(folder)
    list_file = []

    for e_file in list_file_a:
        list_file.append(folder + '/' + e_file)

    dict_src = {}
    dict_des = {}

    for e_file in list_file:

        if "src" in e_file:
            print(e_file)
            line = os.popen('wc -l {}'.format(e_file)).read()
            dict_src[e_file] = int(line.split(' ')[0])
        else:
            line = os.popen('wc -l {}'.format(e_file)).read()
            dict_des[e_file] = int(line.split(' ')[0])

    print(dict_des)
    print(dict_src)

    ls_file_src = list(dict_src.keys())
    for file_path_src in ls_file_src:
        num_file = ((file_path_src.split('/')[-1]).split('.')[0]).split('_')[2]
        file_des = folder + '/' + 'sent_des_' + num_file + '.txt'
        file_src = file_path_src.split('/')[-1]
        # file_new = 'sent_des_' + num_file + '.txt'

        if dict_des[file_des] < dict_src[file_path_src]:
            num = int(dict_des[file_des]) + 1
            new_file_src = os.popen('head -{} {} > {}'.format(num, file_path_src, folder + '/' + 'new_sent_src_' + num_file + '.txt'))
        else:
            num = int(dict_src[file_path_src]) + 1
            new_file_des = os.popen('head -{} {} > {}'.format(num, file_des, folder + '/' + 'new_sent_des_' + num_file + '.txt'))

def creat_vocab():
    lst = [['a', 'à', 'á', 'ạ'],
            ['ă', 'ằ', 'ắ', 'ặ'],
            ['â', 'ầ', 'ấ', 'ậ'],
            ['e', 'è', 'é', 'ẹ'],
            ['ê', 'ề', 'ế', 'ệ'],
            ['o', 'ò', 'ó', 'ọ'],
            ['ô', 'ồ', 'ố', 'ộ'],
            ['ơ', 'ờ', 'ớ', 'ợ'],
            ['i', 'ì', 'í', 'ị'],
            ['u', 'ù', 'ú', 'ụ'],
            ['ư', 'ừ', 'ứ', 'ự'],
            ['y', 'ỳ', 'ý', 'ỵ']]

    vocabs = {}
    for ls in lst:
        for i in ls:

            list_pop = ls[:]
            print(ls)
            list_pop.remove(i)
            print(list_pop)
            vocabs[i] = list_pop

    return vocabs


def check_oov(file_src, file_des):
    list_sent_src = []
    list_sent_des = []
    with open(file_src, 'r') as rf:
        for line in rf.readlines():
            line = line.strip()
            list_sent_src.append(line)

    with open(file_des, 'r') as af:
        for line in af.readlines():
            line = line.strip()
            list_sent_des.append(line)

    for i, e_line_src in enumerate(list_sent_src):
        e_line_src = e_line_src.split(' ')
        cnt_1 = 0
        cnt_2 = 0
        for txt in e_line_src:
            if txt == '<oov>':
                cnt_1 += 1

        for tx in (list_sent_des[i].split(' ')):
            if tx == '<oov>':
                cnt_2 += 1

        if cnt_1 != cnt_2:
            print(i+1)


def check_oov_by_line(line_src, line_des):
    e_line_src = line_src.split(' ')
    cnt_1 = 0
    cnt_2 = 0
    for txt in e_line_src:
        if txt == '<oov>':
            cnt_1 += 1

    for tx in (line_des.split(' ')):
        if tx == '<oov>':
            cnt_2 += 1

    if cnt_1 != cnt_2:
        return True

    return False



if __name__ == '__main__':
    folder = "/home/taibv/Documents/Projects/spellCorection/preprocess/data/train_data"
    # cut_line(folder)
    file_src = 'data/train_data/sent_src.txt'
    file_des = 'data/train_data/sent_des.txt'
    check_oov(file_src, file_des)





