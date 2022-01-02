from datetime import timedelta

import faker
import requests
import json
from urllib.parse import urljoin
import random


URL = "https://restful-booker.herokuapp.com"


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
    check_in, check_out, deposit, first_name, headers, last_name, needs, payload, price = create_booking_json()
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


def test_search_by_name():
    booking_id_list = []
    create_booking_url = urljoin(URL, "booking")
    check_in, check_out, deposit, first_name, headers, last_name, needs, payload, price = create_booking_json()
    create_call = requests.request("POST", create_booking_url, headers=headers, data=payload)
    json_create_call = json.loads(create_call.text)

    search_url = urljoin(URL, f"booking?firstname={first_name}&lastname={last_name}")
    search_call = requests.request("GET", search_url)
    json_search_booking_call = json.loads(search_call.text)

    for entry in json_search_booking_call:
        booking_id_list.append(entry['bookingid'])
    assert json_create_call['bookingid'] in booking_id_list


def test_update_booking():
    create_booking_url = urljoin(URL, "booking")
    check_in, check_out, deposit, first_name, headers, last_name, needs, payload, price = create_booking_json()
    create_call = requests.request("POST", create_booking_url, headers=headers, data=payload)
    json_create_call = json.loads(create_call.text)

    auth_token = create_auth_token('password123')
    update_booking_url = urljoin(URL, f"booking/{json_create_call['bookingid']}")
    c_in, c_out, dep, f_name, haders, l_name, nds, pload, prce = update_booking_json()
    update_call = requests.request("PUT", update_booking_url, headers=haders, data=pload)
    json_response = json.loads(update_call.text)
    assert update_call.status_code == 200
    assert json_response['firstname'] == f_name
    assert json_response['lastname'] == l_name
    assert json_response['totalprice'] == prce
    assert json_response['depositpaid'] == dep
    assert json_response['bookingdates']['checkin'] == str(c_in).split(' ')[0]
    assert json_response['bookingdates']['checkout'] == str(c_out).split(' ')[0]
    assert json_response['additionalneeds'] == nds


def create_booking_json():
    fake = faker.Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    price = random.randint(0, 99999)
    deposit = random.choice([True, False])
    check_in = fake.date_time_this_decade()
    check_out = check_in + timedelta(days=random.randint(0, 240))
    needs = fake.word()
    payload = json.dumps({
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": price,
        "depositpaid": deposit,
        "bookingdates": {
            "checkin": str(check_in),
            "checkout": str(check_out)
        },
        "additionalneeds": needs
    })
    headers = {
        'Content-Type': 'application/json'
    }
    return check_in, check_out, deposit, first_name, headers, last_name, needs, payload, price


def update_booking_json():
    fake = faker.Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    price = random.randint(0, 99999)
    deposit = random.choice([True, False])
    check_in = fake.date_time_this_decade()
    check_out = check_in + timedelta(days=random.randint(0, 240))
    needs = fake.word()
    payload = json.dumps({
        "firstname": first_name,
        "lastname": last_name,
        "totalprice": price,
        "depositpaid": deposit,
        "bookingdates": {
            "checkin": str(check_in),
            "checkout": str(check_out)
        },
        "additionalneeds": needs
    })
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic YWRtaW46cGFzc3dvcmQxMjM=',
        'Content-Type': 'application/json'
    }
    return check_in, check_out, deposit, first_name, headers, last_name, needs, payload, price


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


if __name__ == '__main__':
    # token = create_auth_token(password='password123')
    # https://restful-booker.herokuapp.com/apidoc/index.html
    # random_name = Provider.first_names[random.randint(0, len(Provider.first_names))]
    # test_bookings_return()
    thing = test_update_booking()
