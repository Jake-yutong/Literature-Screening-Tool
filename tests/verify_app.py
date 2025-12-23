import requests
import os

url = 'http://127.0.0.1:5000/screen'
files = {'file': open('../data/test_data.csv', 'rb')}
data = {
    'ta_keywords': 'surgical\npatient\ngame theory',
    'journal_keywords': 'medicine\nphysics'
}

try:
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print("✅ Backend verification SUCCESS!")
        print("Response:", response.json())
    else:
        print(f"❌ Backend verification FAILED. Status: {response.status_code}")
        print("Response:", response.text)
except Exception as e:
    print(f"❌ Connection failed: {e}")
