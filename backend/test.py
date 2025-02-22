import requests

url = "http://127.0.0.1:8000/legal-assistance/"

# List of files to upload (as a list of tuples)
files = [
    ('files', ('Sample Complaint.pdf', open('input/Sample Complaint.pdf', 'rb'), 'application/pdf')),
    ('files', ('Sample Contract.pdf', open('input/Sample Contract.pdf', 'rb'), 'application/pdf'))
]

# The form data (query and option)
data = {
    'query': 'What are the possible legal options for fast retail pvt ltd.?',
    'option': 'Legal Advisory'
}

# Make the request
response = requests.post(url, files=files, data=data)

# Check the response
print(response.json())
