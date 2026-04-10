import json
from datetime import date

english_sentences = [
    "Despite the rain, the team continued the match with unwavering determination.",
    "The novel's protagonist, who had faced countless trials, finally found his voice.",
    "Having completed the course, the students demonstrated an improved ability to reason analytically.",
    "Not until the sunrise did the city reveal its hidden beauty to the weary traveler.",
    "The policy, which was designed to curb emissions, nonetheless faced fierce opposition from industry." 
]

chinese_sentences = [
    "尽管下着雨，球队仍以坚定的意志继续比赛。",
    "小说的主人公经历了无数磨难，终于找到了自己的声音。",
    "完成课程后，学生们展示出更强的分析推理能力。",
    "直到日出时，城市才向疲惫的旅人展现其隐秘之美。",
    "该政策旨在抑制排放，但却遭到了工业界的强烈反对。"
]

gaokao_model_essays = [
    {
        "title": "以青年成长为主题的议论文范文示例",
        "content": "在这个多元世界里，青年应当以批判性思维面对信息洪流。通过自主学习与求真精神，我们能够构建独立判断。..."
    },
    {
        "title": "以科技进步与社会责任的议论文范文示例",
        "content": "科技进步带来便利，但也伴随伦理挑战。我们需要在创新与责任之间取得平衡..."
    }
]

daily_quotes = [
    "知识就是力量，但应用才是智慧。",
    "学习如逆水行舟，不进则退。",
    "写作是思考的涌现。",
    "坚持每日练习，积跬步以至千里。",
    "语言是沟通的桥梁，练习是筑桥的石头。"
]

def seed():
    # This module is a placeholder for seed data; actual seeding happens in app startup.
    return {
        "english_sentences": english_sentences,
        "chinese_sentences": chinese_sentences,
        "gaokao_model_essays": gaokao_model_essays,
        "daily_quotes": daily_quotes,
    }
