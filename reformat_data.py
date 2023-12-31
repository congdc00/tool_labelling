from glob import glob
import os 
from tqdm import tqdm

META_PATH = "./data/metadata/"

if __name__ == "__main__":
    folder_pocess = "./logs/status/*"
    list_voice = glob(folder_pocess)
    os.makedirs(META_PATH, exist_ok = True)

    for voice in list_voice:
        
        voice_path = voice + "/*"
        list_log = glob(voice_path)
        new_line = []
        for log_path in tqdm(list_log):
            
            with open(log_path, 'r') as file:
                for line in file:
                    index, text, path = line.split(",")
                    path = os.path.basename(path)
                    n_line = f"{path}|{text}"
                    new_line.append(n_line)
        
        output_path = f"./data/metadata/{os.path.basename(voice)}.txt"

        with open(output_path, 'w', encoding='utf-8') as file:
            for string in new_line:
                file.write(string + '\n')




