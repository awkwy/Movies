import requests 
import yaml

url = "https://api.themoviedb.org/3/authentication"
with open("config.yml",'r',encoding="utf-8") as file : 
    config = yaml.safe_load(file)

Bearer = config['credentials']['header']
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {Bearer}"
}


response = requests.get(url, headers=headers)

print(response.text)