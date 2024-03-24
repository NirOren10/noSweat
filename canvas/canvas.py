token = "6948~q3tBGdew4kQ9ZPzpN2yuivmEaA80stJ6hTG2pR4VwQKsOupy3JGiAeMI1kudZgmV"

import requests

# Set up API endpoint and parameters
base_url = 'https://rutgers.instructure.com/api/v1'
endpoint = '/courses'
params = {
    'access_token': token,
    # Add any additional parameters as needed
}

# Make GET request to retrieve course data
response = requests.get(base_url + endpoint, params=params)

# Check if request was successful (status code 200)
if response.status_code == 200:
    # Extract and process data from response (assuming JSON format)
    courses = response.json()
    for course in courses:
        # print(course['name'], "ID",course['id'])
        endpoint = f'/courses/{course["id"]}/assignments'
        response = requests.get(base_url + endpoint, params=params)
        assignments = response.json()
        print(course['name'])
        for assignment in assignments:
            print(assignment['name'],assignment['due_at'])
        print("#"*40)
else:
    print('Error:', response.status_code)
    print(response.text)  # Print error message
