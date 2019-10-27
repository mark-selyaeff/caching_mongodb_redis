import os
import socket
import redis
import time
import json
import pymongo
from pymongo import MongoClient

HOST = ''
PORT = 80

print("Waiting for redis and mongo servers...")
time.sleep(5.0)

r = redis.Redis(host='redis', port=6379)
client = MongoClient('mongo', 27017)
db = client.test_database
kvstorage = db.kvstorage

# kvstorage.insert_one(dict)
# kvstorage.find_one({"key": "value"})


def process_json(data):
    try:
        j = json.loads(data)
    except json.decoder.JSONDecodeError as e:
        return json.dumps({"status": "Bad Request"})

    action = j["action"]
    if action == "put":
        # res = r.get(j["key"])
        # r.set(j["key"], j["message"])
        res = kvstorage.find_one({"key": j["key"]})
        if res is not None:
            kvstorage.find_one_and_delete({"_id": res["_id"]})

        kvstorage.insert_one({"key": j["key"], "value": j["message"]})
        if res is not None:
            return json.dumps({"status": "Ok"})
        else:
            return json.dumps({"status": "Created"})

    elif action == "get":  # тут сделать изменения

        if j.get("no-cache"):
            res = kvstorage.find_one({"key": j["key"]})
            if res is None:
                return json.dumps({"status": "Not found"})
            else:
                return json.dumps({"status": "Ok",
                                   "message": res["value"]})

        res = r.get(j["key"])
        if res is None:
            db_res = kvstorage.find_one({"key": j["key"]})
            if db_res is not None:  # no in cache but found in db
                r.set(j["key"], db_res["value"])
                return json.dumps({"status": "Ok",
                                   "message": db_res["value"]})
            return json.dumps({"status": "Not found"})
        else:
            return json.dumps({"status": "Ok",
                               "message": res.decode('utf-8')})

    elif action == "delete":
        res = bool(r.delete(j["key"]))
        if not res:
            return json.dumps({"status": "Not Found"})
        else:
            return json.dumps({"status": "Ok"})

    return json.dumps({"status": "Bad Request"})


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            response = process_json(data)
            # print("Got:", data)
            conn.sendall((response + '\n').encode('utf-8'))
