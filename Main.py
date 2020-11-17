import time
import os
import multiprocessing as mp
import platform
import random

import Util
import Logic
import LogicPrep
############### start to set env ################
WORK_DIR = os.getcwd() + "/"
PROJECT_NAME = WORK_DIR.split("/")[-2]
SYSTEM_NM = platform.system()

if SYSTEM_NM == 'Linux':
    # REAL
    pass
else:
    # DEV
    WORK_DIR = "D:/000_WORK/YuGooSang/20201117/WORK_DIR/"

INPUT_LIST = "./input/input_list.txt"
BASE_SEQ = {'a', 'c', 'g', 't'}


TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
############### end setting env #################


def main():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    input_list = util.read_tsv_ignore_N_line(INPUT_LIST)

    result_list = []
    for val_arr in input_list:
        ori_seq = val_arr[0].upper()
        n_of_mismatch = int(val_arr[1])
        n_of_sub_seq = int(val_arr[2])

        idx_set = logic_prep.make_seq_idx_set(0, len(ori_seq))

        rand_idx_list = []
        for i in range(n_of_sub_seq):
            rand_idx_list.append([random.sample(idx_set, n_of_mismatch)])

        for idx_list in rand_idx_list:
            sub_seq = ori_seq
            for idx_arr in idx_list:
                for i in idx_arr:
                    tmp_set = BASE_SEQ - {ori_seq[i].lower()}
                    sub_seq = logic.swap_char_in_string(sub_seq, i, random.sample(tmp_set, 1)[0])
                result_list.append([ori_seq, sub_seq, len(idx_arr)])

    header = ['ori_seq', 'sub_seq', '#_of_mismatch']
    try:
        util.make_excel(WORK_DIR + '/output/result', header, result_list)
    except Exception as err:
        util.make_tsv(WORK_DIR + '/output/result', header, result_list)


if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    main()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))