import requests

ENDPOINT = "https://opentdb.com/api.php"
PARAMETERS = "amount=15&category=18&type=boolean"
response = requests.get(url=ENDPOINT, params=PARAMETERS)
response.status_code
response.raise_for_status()
question_data = response.json()["results"]
