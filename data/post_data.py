import requests
import json
import os

cur_dir = os.path.dirname(__file__)
infos = json.load(open(os.path.join(cur_dir,"test.json"), encoding="utf8"))

r = requests.get("http://logan:09010163@127.0.0.1:5000/api/v1.0/tokens/")
token = r.json().get("token")
for i,info in enumerate(infos):
    rep = requests.post(f"http://{token}:@127.0.0.1:5000/api/v1.0/infos/",json=info)
    print(rep.status_code)
    if rep.status_code != 201:
        print(rep.text)