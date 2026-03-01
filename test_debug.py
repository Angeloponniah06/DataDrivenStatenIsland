import requests

url = 'http://localhost:8000/api/employment'
params = {'start_year': 2020, 'end_year': 2023}

print(f"Making request to: {url}")
print(f"With params: {params}")

r = requests.get(url, params=params)
print(f"\nFull URL requested: {r.url}")
print(f"Status code: {r.status_code}")

data = r.json()
print(f"\nNumber of records returned: {len(data['series'])}")
print(f"Years in response: {[item['year'] for item in data['series']]}")
