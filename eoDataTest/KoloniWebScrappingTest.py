# define dictionary
payload= {"username": "<USER NAME>",
          "password": "<PASSWORD>"}

import requests
from lxml import html 
session_requests=requests.session()

login_url="https://kolonishare.com/app/partner/login"
result=session_requestions.get(login_url)
tree = html.fromstring(result.text)

result=session_requests.post(
    login_url,
    data=payload,
    headers=dict(referer=login_url))
