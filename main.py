from time import sleep

from src.controller import Controller
from config_parser import Config

config = Config('configs.yaml')

controller = Controller(config.database)

while True:
    controller.fill_trigger()
    controller.fill_emotion()
    print("Update completed")
    sleep(60*60)
