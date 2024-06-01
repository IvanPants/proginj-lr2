from faker import Faker
from schemas import UserSchema

def generate_users():

    fake = Faker()

    users = []

    for _ in range(100000):
        user = {
            'first_name': fake.first_name(),
            'second_name': fake.last_name(),
            'password': fake.password(),
            'login': fake.unique.ascii_email()
        }
        users.append(UserSchema(**user))

    return users




