import faker
import requests
import random
import string

fake = faker.Faker()


def valid_courier():
    return {
        "login": fake.user_name(),
        "password": fake.password(),
        "firstName": fake.first_name()
    }


def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём словарь, чтобы метод мог его вернуть
    login_pass = {}

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier', data=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в словарь логин и пароль курьера
    if response.status_code == 201:
        login_pass['login'] = login
        login_pass['password'] = password

    # возвращаем словарь
    return login_pass


def order_payload():
    return {
        "firstName": fake.first_name(),
        "lastName": fake.last_name(),
        "address": fake.street_address().replace("\n", " "),
        "metroStation": fake.random_int(1, 200),
        "phone": fake.numerify("+7 9## ### ## ##"),
        "rentTime": fake.random_int(1, 7),
        "deliveryDate": fake.date(),
        "comment": fake.sentence(nb_words=4)
    }

