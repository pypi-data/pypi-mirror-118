
import subprocess
import docker
import boto3
import base64
docker_client = docker.from_env()

class Docker:
    def __init__(self):
        pass

    def pull(self, credential):
        print("pull image from docker")
        try:
            aws_client = boto3.client(
                'ecr',
                region_name='ap-northeast-1',
                aws_access_key_id=credential.access_key_id,
                aws_secret_access_key=credential.secret_key,
                aws_session_token=credential.session_token
            )
            resp = aws_client.get_authorization_token()
            token = resp['authorizationData'][0]['authorizationToken']
            token = base64.b64decode(token).decode()
            username, password = token.split(':')
            auth_config = {'username': username, 'password': password}
            image = docker_client.images.pull('307148723122.dkr.ecr.ap-northeast-1.amazonaws.com/map4clitest', auth_config=auth_config)
        except Exception as err:
            print("err", err)

    def run(self):
        print("run docker compose")
        command = ["docker-compose", "up"]
        proc = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in iter(proc.stdout.readline, ''):
            print(line)