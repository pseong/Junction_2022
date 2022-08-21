import os, json

def init():
    secret_file = os.path.join("/home/myuser/project", 'SETTING.json')
    with open(secret_file) as f:
        secrets = json.loads(f.read())
    for key in secrets:
        globals()[key] = secrets[key]