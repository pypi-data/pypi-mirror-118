import subprocess
import pickle
import logging

def bash(cmd):
    import subprocess
    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if ret.returncode != 0:
        logging.warning(ret.stderr)
    return ret.stdout

class Code(object):
    def __init__(self, url):
        self.url = url
    def __call__(self, filename):
        stdout = bash(f"curl {self.url}/{filename}").decode()
        return stdout

class Courier(object):
    def __init__(self, url):
        self.url = url
    def push(self, data, key="uploader"):
        filename = f"/tmp/{key}.temp.pkl"
        with open(filename, 'wb') as fw:
            pickle.dump(data, fw)
        bash(f"curl -X POST {self.url}/upload -F 'files=@{filename}'")
    def fetch(self, key='uploader'):
        filename = f"{key}.temp.pkl"
        stdout = bash(f"curl {self.url}/{filename}")
        return pickle.loads(stdout)

