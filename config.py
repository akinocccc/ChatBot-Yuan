import os

yuan_conf = {
    'username': 'akino',
    'phone': '19129375455',
    'bot_info': '我叫晓潶梓，浙江人，独生女，研究生毕业于伦敦大学，自由职业，喜欢唱歌、跳舞、rap，喜欢温柔体贴的男生'
}

crawler_conf = {
    'save_path': os.path.join(os.path.dirname(__file__), 'prompt_getter/raw_data/'),
    'keywords': ['投资', '赚钱', '工作', '股票', '阅读', '电影']
}