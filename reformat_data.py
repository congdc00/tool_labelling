from glob import glob
import os 
from tqdm import tqdm

if __name__ == "__main__":
    folder_pocess = "./logs/status/*"
    list_voice = glob(folder_pocess)

    for voice in tqdm(list_voice):
        
        voice_path = voice + "/*"
        list_log = glob(voice_path)
        new_line = []
        for log_path in list_log:
            
            with open(log_path, 'r') as file:
                for line in file:
                    index, text, path = line.split(",")
                    path = os.path.basename(path)
                    n_line = f"{path}|{text}"
        
        output_path = f"./data/metadata/{os.path.basename(voice)}.txt"
        with open(output_path, 'w', encoding='utf-8') as file:
            for string in new_line:
                file.write(string + '\n')




