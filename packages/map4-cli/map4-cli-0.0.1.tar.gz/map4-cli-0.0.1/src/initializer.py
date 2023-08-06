
import subprocess
import docker
import shutil
from login import Login
import os

client = docker.from_env()

class Initializer:
    def __init__(self):
        pass

    def create_project(self):
        print("initializer")
        self.create_dir()
        l = Login()
        l.move_to_login_page()

    def create_dir(self):
        if os.path.isdir("./map4_engine_ui") == False:
            new_path = shutil.copytree('./templete', './map4_engine_ui')