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

INPUT_LIST = "./input/input_list.txt"  # 20201117
BASE_NT = {'a', 'c', 'g', 't'}

IN = 'input/'
OU = 'output/'

IN_EXCEL = '5&8_input_201127.xlsx'
ORI_SEQ_STRCTR = [4, 25, 27, -3]
TOTAL_CPU = mp.cpu_count()
MULTI_CNT = int(TOTAL_CPU*0.8)
############### end setting env #################


def main_20201117():
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
                    tmp_set = BASE_NT - {ori_seq[i].lower()}
                    sub_seq = logic.swap_char_in_string(sub_seq, i, random.sample(tmp_set, 1)[0])
                result_list.append([ori_seq, sub_seq, len(idx_arr)])

    header = ['ori_seq', 'sub_seq', '#_of_mismatch']
    try:
        util.make_excel(WORK_DIR + '/output/result', header, result_list)
    except Exception as err:
        util.make_tsv(WORK_DIR + '/output/result', header, result_list)


def main_20201127():
    util = Util.Utils()
    logic_prep = LogicPrep.LogicPreps()
    logic = Logic.Logics()

    df = util.read_excel_to_df(WORK_DIR + IN + IN_EXCEL, '5_input')
    len_df = len(df[df.columns[0]])

    result_list = []
    for i in range(len_df):
        cnt = 0
        ori_seq = df.loc[i][0]
        n_of_mismatch = int(df.loc[i][1])
        n_of_sub_seq = int(df.loc[i][2])

        bp_f = ori_seq[:ORI_SEQ_STRCTR[0]]
        bf_spacer_n_fr_ngg = ori_seq[ORI_SEQ_STRCTR[0]: ORI_SEQ_STRCTR[1]]
        gg_fr_ngg = ori_seq[ORI_SEQ_STRCTR[1]: ORI_SEQ_STRCTR[2]]
        bf_rtt_only = ori_seq[ORI_SEQ_STRCTR[2]: ORI_SEQ_STRCTR[3]]
        bp_b = ori_seq[ORI_SEQ_STRCTR[3]:]

        bf_mm_seq = bf_spacer_n_fr_ngg + bf_rtt_only

        idx_set = logic_prep.make_seq_idx_set(0, len(bf_mm_seq))
        mm_seq_set = set()
        while True:
            if len(mm_seq_set) >= n_of_sub_seq:
                break
            mm_idx_list = random.sample(idx_set, n_of_mismatch)
            af_mm_seq = bf_mm_seq
            for j in mm_idx_list:
                tmp_set = BASE_NT - {bf_mm_seq[j].lower()}
                af_mm_seq = logic.swap_char_in_string(af_mm_seq, j, random.sample(tmp_set, 1)[0])
            mm_seq_set.add(af_mm_seq)
        af_mm_seq_list = list(mm_seq_set)
        for tmp_seq in af_mm_seq_list[: n_of_sub_seq]:
            if cnt == 0:
                result_list.append([ori_seq, bp_f + tmp_seq[:len(bf_spacer_n_fr_ngg)] + gg_fr_ngg + tmp_seq[len(bf_spacer_n_fr_ngg):] + bp_b, n_of_mismatch])
            else:
                result_list.append(['', bp_f + tmp_seq[:len(bf_spacer_n_fr_ngg)] + gg_fr_ngg + tmp_seq[len(bf_spacer_n_fr_ngg):] + bp_b, n_of_mismatch])
            cnt += 1

    util.make_excel(WORK_DIR + OU + '5_input_result', ['ori_seq', 'sub_seq', '#_of_mismatch'], result_list)


if __name__ == '__main__':
    start_time = time.perf_counter()
    print("start [ " + PROJECT_NAME + " ]>>>>>>>>>>>>>>>>>>")
    main_20201127()
    print("::::::::::: %.2f seconds ::::::::::::::" % (time.perf_counter() - start_time))