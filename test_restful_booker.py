import faker
import requests
import json
from urllib.parse import urljoin
import random
from faker.providers.person.en import Provider as person_faker


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


def test_bookings_return():
    url = urljoin(URL, "booking")
    response = requests.request("GET", url)
    assert response.status_code == 200
    assert len(response.text) > 1
    assert json.loads(response.text)[0]['bookingid']


def test_creating_booking():
    url = urljoin(URL, "booking")
    fake = faker.Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    price = random.randint(0, 99999)
    deposit = random.choice([True, False])
    check_in = str(fake.date_time_this_decade())
    check_out = str(fake.date_time_this_decade())
    needs = fake.word()
    payload = json.dumps({
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": price,
        "depositpaid": deposit,
        "bookingdates": {
            "checkin": check_in,
            "checkout": check_out
        },
        "additionalneeds": needs
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    json_response = json.loads(response.text)
    assert response.status_code == 200
    assert json_response['booking']['firstname'] == first_name
    assert json_response['booking']['lastname'] == last_name
    assert json_response['booking']['totalprice'] == price
    assert json_response['booking']['depositpaid'] == deposit
    assert json_response['booking']['bookingdates']['checkin'] == check_in.split(' ')[0]
    assert json_response['booking']['bookingdates']['checkout'] == check_out.split(' ')[0]
    assert json_response['booking']['additionalneeds'] == needs



if __name__ == '__main__':
    # token = create_auth_token(password='password123')
    # https://restful-booker.herokuapp.com/apidoc/index.html
    # random_name = Provider.first_names[random.randint(0, len(Provider.first_names))]
    # test_bookings_return()
    thing = test_creating_booking()
