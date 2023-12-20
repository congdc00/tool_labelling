from schedule import every, repeat
import schedule
from push import start
import yaml
CONFIG_PATH = "./configs/base.yaml"
with open(CONFIG_PATH, 'r') as file:
    configs = yaml.safe_load(file)

@repeat(every(5).seconds)
def auto_label():
    start(configs)

counter = 0 
while True:
    schedule.run_pending()
    counter += 1
    print(f"counter {counter}")
