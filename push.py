from tqdm import tqdm
import requests
import yaml
import os 
import json

CONFIG_PATH = "./configs/base.yaml"

def push(input, configs):
    header = {
        "Authorization": f"{configs['api']['header']['type']} {configs['api']['token']}",
        "Content-Type": configs['api']['header']['content_type']
    }

    content = {
    "app_id": configs['api']['app_id'],
    "callback_url": "https://mydomain/callback",
    "input_text": input,
    "voice_code": configs['api']['content']['voice_code'],
    "audio_type":configs['api']['content']['audio_type'],
    "bitrate": configs['api']['content']['bitrate'] ,
    "speed_rate":configs['api']['content']['speed_rate'] 
    }
    response = requests.post(configs['api']['port'], json=content, headers=header)

    return response.json()

if __name__ == "__main__":
    with open(CONFIG_PATH, 'r') as file:
        configs = yaml.safe_load(file)
    
    input_path = configs["input"]
    name = os.path.basename(input_path).split(".")[0]
    responses_list = []
    with open(configs["input"], 'r') as file:
        for i, line in tqdm(enumerate(file)):
            text = line.replace("\n", "")
            response = push(text, configs)
            response['text'] = text
            response['id'] = i
            responses_list.append(response)
            if i == 2:
                break
    output_path = f"{configs['log']}/init/{name}_{configs['api']['content']['voice_code']}.json"
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(responses_list, json_file, indent=4, ensure_ascii=False)
    print(f"DONE")
