from jupyterhub.spawner import Spawner, LocalProcessSpawner
import requests
import string
import random
import os
import csv
import json
from requests import HTTPError
import sys

# Check that the correct number of arguments was passed to the script
if len(sys.argv) != 6:
    print(
        "Usage: python script.py file_name base_name number_of_users api_token ip_address"
    )
    sys.exit()

# Get the arguments from sys.argv
file_name = sys.argv[1]
base_name = sys.argv[2]
number_of_users = int(sys.argv[3])
api_token = sys.argv[4]
ip_address = sys.argv[5]


class spawner_user:
    def __init__(self, token, username, hubaddress):
        self.token = token
        self.username = username
        self.hubaddress = hubaddress

    def api_request(path, method="get", data=None):
        if data:
            data = json.dumps(data)

        r = requests.request(
            method,
            hub_api + path,
            headers={"Authorization": "token %s" % token},
            data=data,
        )
        try:
            r.raise_for_status()
        except Exception as e:
            try:
                info = r.json()
            except Exception:
                raise e
            if "message" in info:
                # raise nice json error if there was one
                raise HTTPError("%s: %s" % (r.status_code, info["message"])) from None
            else:
                # raise original
                raise e
        if r.text:
            return r.json()
        else:
            return None


def api_request(path, method="get", data=None):
    if data:
        data = json.dumps(data)

    r = requests.request(
        method,
        hub_api + path,
        headers={"Authorization": "token %s" % token},
        data=data,
    )
    try:
        r.raise_for_status()
    except Exception as e:
        try:
            info = r.json()
        except Exception:
            raise e
        if "message" in info:
            # raise nice json error if there was one
            raise HTTPError("%s: %s" % (r.status_code, info["message"])) from None
        else:
            # raise original
            raise e
    if r.text:
        return r.json()
    else:
        return None


class user:
    def __init__(self, name, password, create_command):
        self.name = name
        self.password = password
        self.create_command = create_command


class command_class:
    def __init__(self, get_address, action_address, token, verify=False):
        self.get_address = get_address
        self.action_addess = action_address
        self.token = token
        self.verify = verify
        self.user_list = []

    def list_users(self, base="users"):
        r = requests.get(
            self.get_address + base,
            headers={
                "Authorization": f"token {self.token}",
            },
            verify=self.verify,
        )

        r.raise_for_status()
        user = r.json()
        return user

    def hub_add(self, name):
        r = requests.post(
            self.action_addess + name,
            headers={
                "Authorization": f"token {self.token}",
            },
            verify=self.verify,
        )

        r.raise_for_status()

    def add_user(self, name, N=8):

        # using random.choices()
        # generating random strings
        password = "".join(random.choices(string.ascii_uppercase + string.digits, k=N))

        create_command = f"sudo useradd -p $(openssl passwd {password}) {name}"
        delete_command = f"sudo userdel {name}"

        user_ = user(name, password, create_command)

        os.system(user_.create_command)

        self.hub_add(name)

        user_.token = self.mint_token(name)

        self.user_list.append(user_)

    def delete_user_hub(self, name):
        r = requests.delete(
            self.action_addess + name,
            headers={
                "Authorization": f"token {self.token}",
            },
            verify=self.verify,
        )

        r.raise_for_status()
        return self.list_users()

    def delete_system_user(self, name):
        os.system(f"sudo userdel {name}")

    def delete_all_user_record(self, name):
        self.delete_system_user(name)
        try:
            self.delete_system_user(f"jupyter-{name}")
        except:
            pass
        try:
            self.delete_user_hub(name)
        except:
            pass

    def mint_token(self, name):
        add = f"{name}/tokens"

        r = requests.post(
            self.action_addess + add,
            headers={
                "Authorization": f"token {self.token}",
            },
            verify=self.verify,
        )
        r.raise_for_status()
        return r.json()["token"]


com = command_class(
    f"http://{ip_address}/hub/api/", f"http://{ip_address}/hub/api/users/", api_token
)

for i in range(1, number_of_users + 1):
    try:
        com.add_user(f"{base_name}_{i}")
    except:
        pass

# Open a file in write mode
with open(f"{file_name}.csv", "w", newline="") as file:
    # Create a csv.writer object
    writer = csv.writer(file)

    writer.writerow(["name", "password", "token"])

    # Iterate through the data and write each row to the CSV file
    for i in com.user_list:
        writer.writerow([i.name, i.password, i.token])
