import json
from tqdm import tqdm
import requests
import yaml
import os 


file_name = './logs/init/01_hn_female_ngochuyen_full_48k-fhg.json'

def get_info(request_id, configs):
    port =  configs['api']['port'] + "/" + request_id 
    header = {
        "Authorization": f"{configs['api']['header']['type']} {configs['api']['token']}",
        "Content-Type": configs['api']['header']['content_type']
    }
    response = requests.get(port, headers=header)
    return response.json()


if __name__ == "__main__":
    with open(file_name, 'r', encoding='utf-8') as json_file:
        list_data = json.load(json_file)
    
    with open(CONFIG_PATH, 'r') as file:
        configs = yaml.safe_load(file)
    
    logs = []
    for data in tqdm(list_data):
        request_id = data['result']['request_id']
        id = data['id']

        info = get_info(request_id, configs)
        log = {"id": id, "status": info['result']['status']}
        if info['result']['status'] == "SUCCESS":
            log['audio_link'] = info['result']['audio_link']
        logs.append(log)

    name_log = os.path.basename(file_name)
    log_path = configs['log'] + f"/status/{name_log}"
    with open(log_path, 'w') as json_file:
        json.dump(logs, json_file, indent=4)
    
    print(f"DONE")
