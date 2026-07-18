import requests
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc4NDEwOTU3NCwianRpIjoiYTY5ODcwOGEtYjFlNi00YzdhLTk0ZTQtNzM0NjA5YTNkMTcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImMzNDUwNjkxLWRiNzMtNDlhMi05M2FlLWRlMWVhNmFmNzVjMSIsIm5iZiI6MTc4NDEwOTU3NCwiZXhwIjoxNzg0MTEwNDc0fQ.rMJOtjVKglzppRZrWLPwUXd-5c_xFJ3i_WALu-gB5v0"

with open('faqs.json') as f:
    data = json.load(f)

for faq in data['faqs']:
    response = requests.post(
        'http://localhost:5000/api/faq/create',
        headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'},
        json={'question': faq['question'], 'answer': faq['answer']}
    )
    print(f"Added: {faq['question'][:50]}... - {response.status_code}")

print("All FAQs added!")

