import os

from dotenv import load_dotenv

from app.utils import logger


class Config:

    def __init__(self, filename):
        Config.populate_environment(filename)
        self.config = Config.from_environment()

    def get_config(self):
        return self.config

    @staticmethod
    def populate_environment(filename):
        logger.info("Populating environment variables from config file :", filename)
        load_dotenv(dotenv_path=filename)

    @staticmethod
    def from_environment():
        config = {k[4:]: v for k, v in os.environ.items() if k[:4] == "APP_"}
        return config


config = Config('app/.env').get_config()
logger.info("app configuration :", config)