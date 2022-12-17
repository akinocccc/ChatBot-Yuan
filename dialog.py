import os
import sys
import time

sys.path.append(os.path.abspath(os.curdir))

import paddlehub as hub
from yuan_api.inspurai import Yuan, set_yuan_account, Example
from utils.data_utils import load_prompt, find_index
from config import yuan_conf

class Dialog:
    @classmethod
    def __init__(cls):
        # load prompts
        cls.data = load_prompt()

        # initiate hub module
        cls.simnet_bow = hub.Module(name="simnet_bow")

        # initiate yuan_api api
        set_yuan_account(yuan_conf['username'], yuan_conf['phone'])  # 输入您申请的账号和手机号
        cls.yuan = Yuan(engine='dialog',
                        input_prefix="问：“",
                        input_suffix="”",
                        output_prefix="晓潶梓：“",
                        output_suffix="”",
                        append_output_prefix_to_query=True,
                        topK=5,
                        temperature=0.7,
                        topP=0.8,
                        frequencyPenalty=1.2)

    @classmethod
    def get_similarity(cls, texts):
        start = time.time()
        results = cls.simnet_bow.similarity(texts=texts, use_gpu=False, batch_size=1)
        end = time.time()
        # print(f'computed time: {end - start}s')
        # results.sort(key=lambda k: (k.get('similarity')), reverse=True)
        return results[0]

    @classmethod
    def update_example(cls, prompt):
        count = 0
        for i in range(0, len(cls.data)):
            if count > 5:
                break
            sim_result = cls.get_similarity([[cls.data[i][0]], [prompt]])
            if sim_result['similarity'] >= 0.88:
                count += 1
                print("文本相似度检测：", sim_result)
                inp = sim_result['text_1']
                out = cls.data[find_index(cls.data, sim_result['text_1'])][1]
                cls.yuan.add_example(Example(inp=inp, out=out))
                print(inp, out)
        # i = 0
        # for sim_result in sim_results:
        #     if i < 5 and sim_result['similarity'] >= 0.85:
        #         i += 1
        #         print("文本相似度检测：", sim_result)
        #         inp = sim_result['text_1']
        #         out = cls.data[find_index(cls.data, sim_result['text_1'])][1]
        #         cls.yuan.add_example(Example(inp=inp, out=out))
        #         print(inp, out)
        #     else:
        #         break

    @classmethod
    def remove_example(cls):
        cls.yuan.examples = {}

    @classmethod
    def run(cls):
        print(cls.simnet_bow.get_vocab_path())
        while True:
            cls.yuan.add_example(Example(inp=yuan_conf['bot_info'], out=""))
            prompt = input("问：")
            if prompt.lower() == "q":
                break
            try:
                cls.update_example(prompt)
                response = cls.yuan.submit_API(prompt=prompt, trun="”")
                cls.remove_example()
                print("AI：" + response)
            except Exception as e:
                print("Error !!!! : {}".format(e))
