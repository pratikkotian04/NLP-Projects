from fastapi import FastAPI
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()



@app.get("/create_role")
async def create_role():
    auth = HTTPBasicAuth('username', 'password')
    request_body = {
        "elasticsearch": {
            "cluster": ["all"],
            "indices": [
                {
                    "names": ["chat*"],
                    "privileges": ["read"],
                    "query": "{\"match\": {\"botId\": \"9kC9aMP_u9Ll\"}}"
                }
            ],
        },
        "kibana": [
            {
                "base": [],
                "feature": {
                    "discover": [
                        "all"
                    ],
                    "visualize": [
                        "all"
                    ],
                    "dashboard": [
                        "all"
                    ], },
                "spaces": [
                    "default"
                ]
            }
        ]
    }
    headers = {"Content-type": "application/json", "kbn-xsrf": "true", }
    response = requests.put(
        url="ElasticendPoint/api/security/role/chathist_user", json=request_body, auth=auth, headers=headers)
    print(response.text)
    return {"msg": "Role created successfully"}


@app.get("/get_roles")
async def get_roles():
    auth = HTTPBasicAuth('username', 'password')
    headers = {"Content-type": "application/json", "kbn-xsrf": "true", }
    response = requests.get(
        url="https://asia-south1.gcp.elastic-cloud.com:9243/api/security/role", auth=auth, headers=headers)
    print(response)
    return {"response": response.json(), "msg": "Role fetched successfully"}


@app.get("/assign_user")
async def assign_user():
    auth = HTTPBasicAuth('username', 'password')
    request_body = {
        "password": "j@rV1s",
        "roles": ["chathist_user"],
        "full_name": "Jack Nicholson",
        "email": "jacknich@example.com",
    }
    headers = {"Content-type": "application/json", }
    response = requests.post(
        url="https://asia-south1.gcp.elastic-cloud.com:9243/_security/user/jacknich", json=request_body, auth=auth, headers=headers)
    print(response.json())
    return {"response": response.json(), "msg": "User created successfully"}
