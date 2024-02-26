# -*- coding:UTF-8 -*-
import os

def fuzzy_match_file_name(query, file_path='data/source'):
    candidates = os.listdir(file_path)
    for i in range(len(candidates)):
        if query in candidates[i]:
            return os.path.join(file_path, candidates[i])
    return ""