import json
from generator import generate_mock_data

# This is the template your generator should use for a single post
template = {
    "id": 1,
    "title": "A Day in the Life of a Developer",
    "content": "Today I debugged a complex issue."
}

# Generate a list of 5 posts based on the template
mock_posts = [generate_mock_data(template) for _ in range(5)]

# Print the resulting JSON data to the console
print(json.dumps(mock_posts, indent=2))