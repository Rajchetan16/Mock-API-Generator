from faker import Faker

fake = Faker()

def generate_mock_data(data_template):
    """
    Generates mock data based on a given dictionary template.
    """
    if isinstance(data_template, dict):
        mock_data = {}
        for key, value in data_template.items():
            if "name" in key.lower() or "author" in key.lower():
                mock_data[key] = fake.name()
            elif "email" in key.lower():
                mock_data[key] = fake.email()
            elif "id" in key.lower():
                mock_data[key] = fake.random_int(min=1, max=1000)
            elif "title" in key.lower() or "content" in key.lower() or "text" in key.lower():
                mock_data[key] = fake.text(max_nb_chars=200)
            elif "is_active" in key.lower() or "is_student" in key.lower():
                mock_data[key] = fake.boolean()
            elif isinstance(value, str):
                mock_data[key] = fake.word()
            elif isinstance(value, int):
                mock_data[key] = fake.random_int()
            elif isinstance(value, float):
                mock_data[key] = fake.random_int() / 100
            elif isinstance(value, bool):
                mock_data[key] = fake.boolean()
            else:
                mock_data[key] = generate_mock_data(value)
        return mock_data
    elif isinstance(data_template, list):
        # We'll generate 5 mock items as a list
        return [generate_mock_data(data_template[0]) for _ in range(5)]
    else:
        return data_template
        
if __name__ == "__main__":
    template = {
        "id": 1,
        "title": "A Day in the Life of a Developer",
        "content": "Today I debugged a complex issue...",
        "author": {
            "name": "Jane Doe",
            "email": "jane.doe@example.com"
        }
    }
    generated_data = generate_mock_data(template)
    print("Generated Mock Data:")
    print(generated_data)