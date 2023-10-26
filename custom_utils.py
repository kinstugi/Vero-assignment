import requests
import datetime

def login()->str:
    url = "https://api.baubuddy.de/index.php/login"
    payload = {
        "username": "365",
        "password": "1"
    }
    headers = {
        "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
        "Content-Type": "application/json"
    }
    response = requests.post(url= url, json= payload, headers= headers)
    if response.status_code != 200: 
        raise Exception("failed to log in")
    responseBody = response.json()
    return responseBody['oauth']['access_token']

def fetch_data(token: str):
    url = "https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url= url, headers= headers)
    if response.status_code == 401:
        raise Exception("auth token has expired")
    return response.json()

def resolve_color_code(labelId: str, token: str)->dict:
    url = f'https://api.baubuddy.de/dev/index.php/v1/labels/{labelId}'
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(url = url, headers= headers)
    if  200 <= res.status_code <= 299: 
        return res.json()
    raise Exception("auth token has expired")

def months_passed(date_string: str)->float:
    date_object = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    today = datetime.datetime.today()
    diff = today - date_object
    num_months = diff.days / 30
    return num_months
