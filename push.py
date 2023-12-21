from tqdm import tqdm
import requests
import yaml
import os 
import json

CONFIG_PATH = "./configs/base.yaml"
SCRIPT_PATH = "./scripts/change_voice_01.txt"
MODE = "dev"
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

def load_input(input_path):
    with open(input_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

def save_data(log_path, content):
    with open(log_path, 'w', encoding='utf-8') as json_file:
        json.dump(content, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    with open(CONFIG_PATH, 'r') as file:
        configs = yaml.safe_load(file)
    
    input_path = configs["input"]
    name = os.path.basename(input_path).split(".")[0]
    
     
    data = load_input(configs["input"])
    voices = load_input(SCRIPT_PATH) 

    for j, voice in enumerate(voices):
        configs["api"]["content"]["voice_code"] = voice

        output_path = f"{configs['log']}/init/{name}_{configs['api']['content']['voice_code']}"
        os.makedirs(output_path, exist_ok = True)

        for i, line in enumerate(data):
            log_path = f"{configs['log']}/init/{name}_{configs['api']['content']['voice_code']}/{i}.json" 

            # skip 
            if os.path.exists(log_path):
                continue

            # run
            text = line.replace("\n", "")
            if len(text) > 0: 
                response = push(text, configs)
                response['text'] = text
                response['id'] = i
                save_data(log_path, response)
            
            # test
            if MODE == "dev":
                if i >=2:
                    break

        
    print(f"DONE {len(voices)} voices and {len(data)} text")
