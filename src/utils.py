import json
import yaml
from typing import List, Dict
import glob
import os

def calculate_id(file_root):
    file_list = glob.glob(os.path.join(file_root, "motion", "*.yml"))
    return len(file_list) + 1

model_map = {
    "google/gemini-pro-1.5": "GeminiPro15",
    "google/gemini-flash-1.5": "GeminiFlash15",
    "claude-3-5-haiku-20241022": "ClaudeHaiku3",
    "claude-3-5-sonnet-20241022": "ClaudeSonnet35",
    "gpt-4o-mini": "GPT4oMini",
    "gpt-4o": "GPT4o",
    "deepseek-chat": "DeepSeekChat",
    "qwen/qwen-2-72b-instruct": "Qwen72b",
    "glm-4-air": "GLM4",
    "human": "human",
    "baseline": "baseline",
}
def save_zh_result(preset: str, topic: str, messages: List[Dict], pos_model: str, neg_model: str, round_num: int):
    template = dict(
        motion = topic,
        pro_side = [dict(name = "正方")],
        con_side = [dict(name = "反方")],
        pro_model = [dict(model = pos_model)],
        con_model = [dict(model = neg_model)],
        info_slide = "正反双方的举证责任相同",
    )

    round_num *= 2
    speech = []
    for i in range(round_num):
        if i % 2 == 0:
            debater_name = "正方"
        else:
            debater_name = "反方"
        speech.append(dict(
            debater_name = debater_name,
            content = messages[i]["content"]
        ))
    
    file_root = os.path.join("output", preset)
    os.makedirs(os.path.join(file_root, "motion"), exist_ok=True)
    os.makedirs(os.path.join(file_root, "speech"), exist_ok=True)
    
    ids = str(calculate_id(file_root)).zfill(4)

    try:
        pos_model = model_map[pos_model]
        neg_model = model_map[neg_model]
    except KeyError:
        raise ValueError("Model not found")
    except Exception as e:
        raise e
    
    yaml.dump(
        template,
        open(f"{file_root}/motion/{preset}_zh_{pos_model}_{neg_model}_{ids}.yml", "w"),
        allow_unicode=True, sort_keys=False,
    )
    
    yaml.dump(
        speech,
        open(f"{file_root}/speech/{preset}_zh_{pos_model}_{neg_model}_{ids}.yml", "w"),
        allow_unicode=True, sort_keys=False,
    )
    
    with open(f"{file_root}/motion/motion_list.txt", "a") as f:
        content = f"{preset}_zh_{pos_model}_{neg_model}_{ids}  {topic}\n"
        f.write(content)

    os.makedirs(os.path.join(file_root, f"agent/{preset}_zh_{pos_model}_{neg_model}_{ids}"), exist_ok=True)
    last_lines = []
    # round_num *= 2
    with open("log/agent/log.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():  # 跳过空行
                last_lines.append(line)
                if len(last_lines) > round_num:
                    last_lines.pop(0)
    
    if last_lines:
        # 解析JSON
        # yaml.dump(
        #     last_line,
        #     open(f"{file_root}/agent/{preset}_zh_{pos_model}_{neg_model}_{ids}/agent_history.yml", "w"),
        #     allow_unicode=True, sort_keys=False,
        # )
        for i in range(len(last_lines)):
            chat_data = json.loads(last_lines[i])
            chat_history = chat_data['chat_history']
            
            # 将chat_history格式化为易读的文本
            formatted_history = []
            for message in chat_history:
                role = message.get('role', '')
                name = message.get('name', '')
                content = message.get('content', '')
                
                formatted_message = f"Role: {role}\nName: {name}\nContent:\n{content}\n{'='*50}\n"
                formatted_history.append(formatted_message)
            formatted_history_full = '\n'.join(formatted_history)
            with open(f"{file_root}/agent/{preset}_zh_{pos_model}_{neg_model}_{ids}/agent_history_{i}.txt", 'w', encoding='utf-8') as f:
                f.write(formatted_history_full)
