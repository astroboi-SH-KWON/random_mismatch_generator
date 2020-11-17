
from astroboi_bio_tools.ToolLogic import ToolLogics
class Logics(ToolLogics):
    def swap_char_in_string(self, trgt_seq, i, ch):
        return trgt_seq[:i] + ch + trgt_seq[i + 1:]
