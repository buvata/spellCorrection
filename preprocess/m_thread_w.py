from queue import Queue
import threading
from spellCorrection.preprocess.aug_dataset_v2 import *
from spellCorrection.preprocess.handle_text import *
from tqdm import tqdm

exitFlag = 0

class myThread (threading.Thread):

    def __init__(self, thread_name, queue, file_src, file_des, lock_file, pbar):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.queue = queue
        self.file_src = file_src
        self.file_des = file_des
        self.lock_file = lock_file
        self.pbar = pbar

    def run(self):
        with open('log_error.txt', 'w') as wf:
            while not self.queue.empty():
                sent = self.queue.get()
                self.pbar.update(1)
                try:
                    l_a = augment_data(sent)
                except Exception as e:
                    wf.write("Failed {0}: {1}\n".format(str(sent), str(e)))
                    l_a = '{}||{}'.format(sent, sent)
                    l_a = [l_a]

                self.lock_file.acquire()

                for e_sent in l_a:
                    # print("thread {} write: ", self.thread_name)
                    sent_src = e_sent.split('||')[0]
                    sent_des = e_sent.split('||')[1]
                    self.file_src.write(sent_src + "\n")
                    self.file_des.write(sent_des + "\n")

                self.lock_file.release()


def run_multi_thread(file_data, file_src, file_des):
    lock_common = threading.Lock()
    t_a = open(file_src, "a")
    t_b = open(file_des, "a")

    queue_sent = Queue(maxsize=-1)

    list_sent = []
    with open(file_data, 'r') as rf:
        for line in rf.readlines():
            line = line.strip()
            line = norm_text(line)
            line = line.lower()
            line = remove_multi_space(line)
            line = link_punc(line)
            if 5 < len(line.split(' ')) < 256:
                list_sent.append(line)

    pbar = tqdm(total=len(list_sent), desc='abc')

    for sent in list_sent:
        queue_sent.put(sent)

    l_threads = []
    for i in range(3):
        e_thread = myThread("thread_{}".format(i + 1),
                            queue_sent,
                            t_a,
                            t_b,
                            lock_common, pbar)

        l_threads.append(e_thread)
        e_thread.start()

    for i in range(3):
        l_threads[i].join()


if __name__ == '__main__':
   file_data = 'data/train_data/demo-full.txt'
   file_src = 'data/train_data/sent_src.txt'
   file_des = 'data/train_data/sent_des.txt'
   run_multi_thread(file_data,file_src, file_des)