
import requests
import json

URL = 'http://127.0.0.1:8000/crud/'


#get data
def get(id=None):
    data = {}
    if id is not None:
        data = {'id': id}
    jdata = json.dumps(data)
    r = requests.get(url=URL, data=jdata)
    data = r.json()
    print(data)

#get_data()

def post():
    data = {'name': 'mayank','age' :22,'job_type': 'java','address' : 'pbr',}
    #jdata = json.dumps(data)
    r = requests.post(url=URL, data=data)
    data = r.json()
    print(data)
# Run 
#post_data()
#get_data()

def update():
    data = {
        'id': 45, 
        'name': 'manshi',
        'age' :25,
        'job_type': 'js',
        'address' : 'rjt'
        }
    jdata = json.dumps(data)
    r = requests.put(url=URL, data=jdata)
    data = r.json()
    print(data)
# Run
#update_data()
#get_data()

def delete():
    data = {'id': 44}
    jdata = json.dumps(data)
    r = requests.delete(url=URL, data=jdata)
    data = r.json()
    print(data)

# run 
update()
#delete()
#post()
get()
