import json
import requests
import yaml
import os 
import time
CONFIG_PATH = "./configs/base.yaml"
SCRIPT_PATH = "./scripts/change_voice_01.txt"
MODE = "dev"
file_name = './logs/status/01_hn_female_ngochuyen_full_48k-fhg.json'

def load_input(input_path):
    with open(input_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines
def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
def get_info(request_id, configs):
    port =  configs['api']['port'] + "/" + request_id 
    header = {
        "Authorization": f"{configs['api']['header']['type']} {configs['api']['token']}",
        "Content-Type": configs['api']['header']['content_type']
    }
    response = requests.get(port, headers=header)
    return response.json()
if __name__ == "__main__":
    with open(CONFIG_PATH, 'r') as file:
        configs = yaml.safe_load(file)
    
    input_path = configs["input"]
    name = os.path.basename(input_path).split(".")[0]
     
    data = load_input(configs["input"])
    voices = load_input(SCRIPT_PATH) 

    for j, voice in enumerate(voices):
        configs["api"]["content"]["voice_code"] = voice
        log_pre_path = f"{configs['log']}/init/{name}_{configs['api']['content']['voice_code']}"
        status_path = log_pre_path.replace("init", "status")
        os.makedirs(status_path, exist_ok=True)
        output_path  = f"./data/output/{name}_{configs['api']['content']['voice_code']}"
        os.makedirs(output_path, exist_ok=True)
 
        for i, line in enumerate(data):
           
            log_path = f"{log_pre_path}/{i}.json"
            save_path = output_path + "/" + f"{i}.wav"
            
            while not os.path.exists(log_path):
                time.sleep(3)
                print(f"wait pull {log_path}")
            # crawl data
            if not os.path.exists(save_path):
               
                ss_path = f"{status_path}/{i}.txt"
                info_1 = load_json_file(log_path)
                
                is_success = False
                n_loop = 0
                while not is_success:

                    request_id = info_1['result']['request_id']
                    info_2 = get_info(request_id, configs)
                    if info_2['result']['status'] == "SUCCESS":
                        url = info_2['result']['audio_link']
                        response = requests.get(url)
                        if response.status_code == 200:
                           
                            with open(save_path, 'wb') as file:
                                file.write(response.content)

                            with open(ss_path, 'w') as file:
                                content = f"{i}, {info_1['text']}, {save_path}"
                                file.write(content)

                            is_success = True
                            print(f"Done")
                    else:
                       
                        print(f"wait process {log_path}")
                        time.sleep(5)
                        
                    if n_loop <1:
                        n_loop += 1 
                    else: 
                        break
def check_done():
    return True


@repeat(every(5).seconds)
def auto_push():
    main()

if __name__ == "__main__":
   
    while True:
        is_continue = check_done()
        if not is_continue:
            break

        schedule.run_pending()
