import pandas as pd


from astroboi_bio_tools.ToolUtil import ToolUtils
class Utils(ToolUtils):
    # conda install -c anaconda xlrd
    def get_sheet_names(self, path):
        df = pd.read_excel(path, None)
        return [k for k in df.keys()]

    def read_excel_to_df(self, path, sheet_name='Sheet1'):
        return pd.read_excel(path, sheet_name=sheet_name)