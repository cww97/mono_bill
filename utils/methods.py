# -*- coding:UTF-8 -*-
import os
from pandas import DataFrame as df


def fuzzy_match_file_name(query, file_path='data/source'):
    candidates = os.listdir(file_path)
    for i in range(len(candidates)):
        if query in candidates[i]:
            return os.path.join(file_path, candidates[i])

def strip_in_data(df):
    # import pdb; pdb.set_trace()
    df = df.rename(columns={column_name: column_name.strip().replace('/', '') for column_name in df.columns})
    df = df.apply(lambda x: x.str.strip().replace('\t', '') if x.dtype == "object" else x)
    return df