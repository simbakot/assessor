from time import sleep

from src.controller import Controller
from src.database import Database
from config_parser import Config

config = Config('configs.yaml')
database = Database(config.database)

controller = Controller()

while True:
    controller.fill_trigger(database)
    controller.fill_emotion(database)
    print("Update completed")
    sleep(60*60)
