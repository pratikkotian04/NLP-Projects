from fastapi import FastAPI
from elasticsearch import Elasticsearch
import requests
from requests.auth import HTTPBasicAuth

app = FastAPI()

es = Elasticsearch(cloud_id="engagely-deployment:YXNpYS1zb3V0aDEuZ2NwLmVsYXN0aWMtY2xvdWQuY29tJGQyMDhhNDBhYzU2ZDQ3ZmFhNzdlODFlZDRmMzlmODJkJGNhYmUxOTdkYzQ2ZTQ3ODQ5OGUzMDE2MGFkNWRlMGI5",
                   http_auth=('elastic', 'Id2IxE0eqbJWXB8yB04RwMTr'))


@app.get("/create_role")
async def create_role():
    auth = HTTPBasicAuth('elastic', 'Id2IxE0eqbJWXB8yB04RwMTr')
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
        url="https://cabe197dc46e478498e30160ad5de0b9.asia-south1.gcp.elastic-cloud.com:9243/api/security/role/chathist_user", json=request_body, auth=auth, headers=headers)
    print(response.text)
    return {"msg": "Role created successfully"}


@app.get("/get_roles")
async def get_roles():
    auth = HTTPBasicAuth('elastic', 'Id2IxE0eqbJWXB8yB04RwMTr')
    headers = {"Content-type": "application/json", "kbn-xsrf": "true", }
    response = requests.get(
        url="https://cabe197dc46e478498e30160ad5de0b9.asia-south1.gcp.elastic-cloud.com:9243/api/security/role", auth=auth, headers=headers)
    print(response)
    return {"response": response.json(), "msg": "Role fetched successfully"}


@app.get("/assign_user")
async def assign_user():
    auth = HTTPBasicAuth('elastic', 'Id2IxE0eqbJWXB8yB04RwMTr')
    request_body = {
        "password": "j@rV1s",
        "roles": ["chathist_user"],
        "full_name": "Jack Nicholson",
        "email": "jacknich@example.com",
    }
    headers = {"Content-type": "application/json", }
    response = requests.post(
        url="https://d208a40ac56d47faa77e81ed4f39f82d.asia-south1.gcp.elastic-cloud.com:9243/_security/user/jacknich", json=request_body, auth=auth, headers=headers)
    print(response.json())
    return {"response": response.json(), "msg": "User created successfully"}
