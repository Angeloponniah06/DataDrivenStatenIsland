import requests

print("Testing Date Range Filters:\n")

# Test 1: Employment data with date range
print("1. Employment API (2020-2023):")
r = requests.get('http://localhost:8000/api/employment', params={'start_year': 2020, 'end_year': 2023})
data = r.json()
for item in data['series']:
    print(f"   {item['year']}: {item['unemployment_rate']}% unemployment, {item['employment_rate']}% employment")

print("\n2. Business API (2021-2024):")
r = requests.get('http://localhost:8000/api/business', params={'start_year': 2021, 'end_year': 2024})
data = r.json()
for item in data['series']:
    print(f"   {item['year']}: {item['new_businesses']} new, {item['closed_businesses']} closed, {item['net_change']} net")

print("\n3. Employment API (no filter - should return all):")
r = requests.get('http://localhost:8000/api/employment')
data = r.json()
print(f"   Total records: {len(data['series'])}")
print(f"   Years: {[item['year'] for item in data['series']]}")
