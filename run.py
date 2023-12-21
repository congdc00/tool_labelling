from schedule import every, repeat
import schedule
from push import start
import yaml
CONFIG_PATH = "./configs/base.yaml"
with open(CONFIG_PATH, 'r') as file:
    configs = yaml.safe_load(file)
counter = 0 
    counter += 1
    print(f"counter {counter}")
