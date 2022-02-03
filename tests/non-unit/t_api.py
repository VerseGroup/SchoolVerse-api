import requests

URL = "http://localhost:8000"

def t_scrape():
    eurl = URL + "/scrape"
    data = {
        "user_id": 1,
        "platform_code": "sc"
    }
    r = requests.post(eurl, data=data)
    assert r.status_code == 200


