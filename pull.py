import json
import requests
import yaml
import os 
CONFIG_PATH = "./configs/base.yaml"
file_name = './logs/status/01_hn_female_ngochuyen_full_48k-fhg.json'
if __name__ == "__main__":
    with open(file_name, 'r', encoding='utf-8') as json_file:
        list_data = json.load(json_file)
    
    with open(CONFIG_PATH, 'r') as file:
        configs = yaml.safe_load(file)

    output_name  = os.path.basename(file_name).split(".")[0]
    output_path = configs['output'] + "/" + output_name + "/"
    os.makedirs(output_path, exist_ok = True)
    
    for data in list_data:
        if data['status'] == 'SUCCESS':
            url = data["audio_link"]
            response = requests.get(url)
            if response.status_code == 200:
                save_path = output_path + "/" + f"{data['id']}.mp3"
                with open(save_path, 'wb') as file:
                    file.write(response.content)
