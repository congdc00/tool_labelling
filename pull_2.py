import json
import requests
import yaml
import os 
import time
from schedule import every, repeat
import schedule
import threading
CONFIG_PATH = "./configs/base.yaml"
SCRIPT_PATH = "./scripts/change_voice_02.txt"
MODE = "dev"
file_name = './logs/status/01_hn_female_ngochuyen_full_48k-fhg.json'
NUM_WORKER = 2
BATCH_SIZE = 10

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
    while True:
        response = requests.get(port, headers=header)
        try:
            result = response.json()
            return result
        except:
            time.sleep(5)

# worker
class Worker:
    def __init__(self, name, type_worker='sequential'):
        self.is_working = False
        self.name_worker = str(name)
        self.type_worker = type_worker
        if type_worker == 'sequential':
            self.limit_loop = 3 
        else:
            self.limit_loop = 0 

    def get_status(self):
        return self.is_working 
    
    def check_info(self, log_path):
        loop = 0
        while not os.path.exists(log_path):
            time.sleep(3)
            print(f"Worker {self.name_worker} wait pull {log_path}")
            loop += 1 
            if loop >= self.limit_loop:
                return False
        return True

    def crawl_data(self, log_path, save_path, configs, status_path, index):
        if os.path.exists(save_path):
            return True
        
        # load status 
        info_1 = load_json_file(log_path)
        if info_1['status'] == 0:
            return False
        
        # load info download 
        request_id = info_1['result']['request_id']
        info_2 = get_info(request_id, configs)

        is_success = False
        loop = 0
        while not is_success:
            if info_2['result']['status'] == "SUCCESS":
                url = info_2['result']['audio_link']
                response = requests.get(url)
                if response.status_code == 200:
                    # save audio
                    with open(save_path, 'wb') as file:
                        file.write(response.content)
                
                    # save status
                    ss_path = f"{status_path}/{index}.txt"
                    with open(ss_path, 'w') as file:
                        content = f"{index}, {info_1['text']}, {save_path}"
                        file.write(content)
                        is_success = True
                    print(f"Worker {self.name_worker} done {log_path}")

            else:
                print(f"Worker {self.name_worker} wait vbee process {log_path}")
                time.sleep(5)
                        
            loop += 1 
            if loop >= self.limit_loop:
                break
        return True
    
    def auto_crawl(self, configs, index, log_path, save_path, status_path):
        self.is_working = True
        if self.check_info(log_path):
            self.crawl_data(log_path, save_path, configs, status_path, index)
        self.is_working = False

def process_batch(worker,configs, log_pre_path, status_path, batch_data, i_start, output_path):
    i = i_start
    for data in batch_data:
        log_path = f"{log_pre_path}/{i}.json"
        save_path = output_path + "/" + f"{i}.wav"

        worker.auto_crawl(configs, i, log_path, save_path, status_path) 
        i+=1

def main():
    with open(CONFIG_PATH, 'r') as file:
        configs = yaml.safe_load(file)
    
    input_path = configs["input"]
    name = os.path.basename(input_path).split(".")[0]

    data = load_input(configs["input"])
    voices = load_input(SCRIPT_PATH) 
    
    list_worker = []

    # init worker sequential
    worker = Worker(name = 0)
    list_worker.append(worker) 

    # init worker random 
    for i in range(1, NUM_WORKER):
        worker = Worker(name = i, type_worker = "random")
        list_worker.append(worker)

    for j, voice in enumerate(voices):
        configs["api"]["content"]["voice_code"] = voice
        log_pre_path = f"{configs['log']}/init/{name}_{configs['api']['content']['voice_code']}"
        status_path = log_pre_path.replace("init", "status")
        os.makedirs(status_path, exist_ok=True)
        output_path  = f"./data/output/{name}_{configs['api']['content']['voice_code']}"
        os.makedirs(output_path, exist_ok=True)
        
        i_batch = 0 
        while len(data) - i_batch*BATCH_SIZE > 0:
            i_start = i_batch*BATCH_SIZE
            if len(data) - i_batch*BATCH_SIZE <= BATCH_SIZE:
                data_batch = data[i_start:]
            else:
                data_batch = data[i_start:i_start+BATCH_SIZE]

            is_work = False
            while not is_work:
                for worker in list_worker:
                    if not worker.get_status():
                        session_work = threading.Thread(target= process_batch, args=(worker,configs, log_pre_path, status_path, data_batch, i_start, output_path))
                        session_work.start()
                        is_work = True
                        break
                time.sleep(5)

            i_batch +=1           

                                
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
