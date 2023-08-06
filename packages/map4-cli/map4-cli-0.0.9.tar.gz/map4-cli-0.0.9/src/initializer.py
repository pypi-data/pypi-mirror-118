
import subprocess
import docker
import shutil
from .login import Login
import os
from pathlib import Path

client = docker.from_env()

class Initializer:
    def __init__(self):
        pass

    def create_project(self):
        self.create_dir()
        l = Login()
        l.move_to_login_page()

    def create_dir(self):
        templete_dir_path = Path(os.path.dirname(__file__)).joinpath('..', 'templete').resolve()
        create_dir_path = Path(os.getcwd()).joinpath("map4_engine_ui").resolve()
        if os.path.isdir(create_dir_path) == False:
            new_path = shutil.copytree(templete_dir_path, create_dir_path)