import multiprocessing
from multiprocessing import Process, Pool
from spellCorection.preprocess.aug_dataset_v2 import *
from tqdm import *
from p_tqdm import p_map

def multi_augment(sent):
    ls_text = augment_data(sent)
    return ls_text


def write_file_des_src(list_text, file_src, file_des):
    i = 0
    ls_text_src, ls_text_des = [], []
    for ls_text in list_text:
        for txt in ls_text:
            ls_text_src.append(txt.split('||')[0])
            ls_text_des.append(txt.split('||')[1])
            i += 1
            print(i)

    with open(file_src, 'w') as wf:
        for txt in ls_text_src:
            wf.write('{}\n'.format(txt))

    with open(file_des, 'w') as wf:
        for txt in ls_text_des:
            wf.write('{}\n'.format(txt))


if __name__ == '__main__':

    file_src = "preprocess/data/train_data/sent_src.txt"
    file_des = "/home/taibv/Documents/Projects/spellCorection/preprocess/data/train_data/sent_des.txt"
    file_data = "/home/taibv/Documents/Projects/spellCorection/preprocess/data/train_data/bao_moi"

    list_sent = []
    with open(file_data, 'r') as rf:
        for line in rf.readlines():
            line = line.strip()
            line = norm_text(line)
            line = line.lower()
            line = remove_multi_space(line)
            line = link_punc(line)
            list_sent.append(line)


    result = p_map(augment_data, list_sent, num_cpus=3)
        # write_file_des_src(result, file_src, file_des)
    print(result)


    write_file_des_src(result, file_src, file_des)


