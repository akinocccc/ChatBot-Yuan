import json
import os

def load_prompt():
    base_path = 'D:/projects/ChatBot-Yuan/prompt_getter/raw_data/'
    file_list = os.listdir(base_path)
    data = []
    # print(file_list)
    for cur_file in file_list:
        with open(base_path + cur_file, 'a+', encoding='utf-8') as f:
            f.seek(0)
            line = f.readline()
            while len(line) > 0:
                # print(line)
                data.append(json.loads(line))
                line = f.readline()
            f.close()
    print('样本：', len(data))
    return data

def find_index(arr, text):
    for i in range(0, len(arr)):
        if arr[i][0] == text:
            return i
    return -1
