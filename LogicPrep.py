
from astroboi_bio_tools.ToolLogicPrep import ToolLogicPreps
class LogicPreps(ToolLogicPreps):
    def make_seq_idx_set(self, st_idx, en_idx):
        result_set = set()
        for idx in range(st_idx, en_idx):
            result_set.add(idx)
        return result_set
