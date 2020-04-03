import argparse
from m_thread_w import *

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--path_data", type=str, default='',
                        help="path data")

    parser.add_argument("--path_save_src", type=str, default='',
                        help="save file src")

    parser.add_argument("--path_save_des", type=str, default='',
                        help="save file des")

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    path_data = args.path_data
    path_save_src = args.path_save_src
    path_save_des = args.path_save_des

    run_multi_thread(path_data, path_save_src, path_save_des)
