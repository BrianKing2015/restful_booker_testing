import requests
import json
from urllib.parse import urljoin
import random
from faker.providers.person.en import Provider

URL = "https://restful-booker.herokuapp.com"


def create_auth_token(password):
    url = urljoin(URL, "auth")
    payload = json.dumps({
      "username": "admin",
      "password": password
    })
    headers = {
      'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)['token']


def test_service_up():
    url = urljoin(URL, "ping")
    response = requests.request("GET", url)
    assert response.status_code == 201
    assert response.text == "Created"



if __name__ == '__main__':
    # token = create_auth_token(url="https://restful-booker.herokuapp.com/auth", password='password123')
    # https://restful-booker.herokuapp.com/apidoc/index.html
    # random_name = Provider.first_names[random.randint(0, len(Provider.first_names))]
    test_service_up()