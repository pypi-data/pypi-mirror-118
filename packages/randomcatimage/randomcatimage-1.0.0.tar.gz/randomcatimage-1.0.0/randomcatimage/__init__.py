import requests

headers = {"x-api-key": "cc0eb636-fcc2-4522-ad8a-f2319898a5c3"}

def getCat(mime):
    if mime == 'png':
        response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=png', headers=headers)
        data = response.json()
        d = data[0]
    elif mime == 'jpg':
        response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=jpg', headers=headers)
        data = response.json()
        d = data[0]
    elif mime == 'gif':
        response = requests.get('https://api.thecatapi.com/v1/images/search?mime_types=gif', headers=headers)
        data = response.json()
        d = data[0]
    return d['url']
