import json
from typing import Optional
import requests

class OneAccount:

    def __init__(self, engine):
        self.verify_url: str = "https://api.oneaccount.app/widget/verify"
        self.uuid = None
        self.engine = engine
        self.auth_header = None

    def verify(self) -> bool:
        request = requests.post(self.verify_url, headers={
            "Authorization": f"{self.auth_header}",
            "Content-Type": "application/json",
        }, json={
            "uuid": self.uuid
        })

        result = request.json()
        return request.status_code == 200 and result["success"]

    async def auth(self, request) -> Optional[dict]:
        try:
            self.auth_header = request.headers['Authorization']
        except KeyError:
            result = await request.json()
            self.save(result)
            return None
        else:
            result = await request.json()
            try:
                self.uuid = result["uuid"]
            except KeyError:
                raise Exception("Uuid key not found")
            return self.authorize()

    def save(self, body: dict):
        if not body:
            raise Exception("Body is either empty or not provided")
        if "uuid" not in body:
            raise Exception("Uuid could not be found in the body")

        str_body = json.dumps(body)
        try:
            self.engine.set(body["uuid"], str_body)
        except Exception as e:
            raise Exception(f"Engine: Set method returned an error {e}")

    def authorize(self) -> dict:
        if not self.auth_header or not self.auth_header.startswith("Bearer "):
            raise Exception("Authorization token is not provided")
        if not self.uuid:
            raise Exception("Uuid is not provided")

        try:
            data: str = self.engine.get(self.uuid)
            if not data:
                raise Exception("Engine: Get method did not return any data")

            result = json.loads(data)

        except Exception as e:
            raise Exception(f"Engine parsing error: {e}")

        if not self.verify():
            raise Exception("One account verification failed")

        return result


class InMemoryEngine:

    def __init__(self):
        self.data = {}

    def set(self, key: str, value: str) -> None:
        self.data[key] = value

    def get(self, key: str) -> str:
        return self.data[key]

