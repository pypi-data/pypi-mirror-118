import click
from .login import Login
from .initializer import Initializer
from .docker_process import Docker


@click.group()
def cmd():
    pass


@cmd.command()
def run():
    click.echo('Run')
    d = Docker()
    d.run()

@cmd.command()
def init():
    i = Initializer()
    i.create_project()

@cmd.command()
def login():
    l = Login()
    l.move_to_login_page()

@cmd.command()
def login2():
    l = Login()
    l.admin_initiate_auth("testusers", "Testuser_1")

@cmd.command()
def pull():
    click.echo('Pull images')
    d = Docker()
    d.pull()

def main():
    cmd()
    
if __name__ == '__main__':
    main()