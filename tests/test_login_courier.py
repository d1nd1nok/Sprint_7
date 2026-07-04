import allure
import requests
import pytest

from Sprint_7.src.helpers import register_new_courier_and_return_login_password, valid_courier
from src.urls import LOGIN_COURIER


class TestLoginCourier:

    @allure.title("Курьер может авторизоваться и успешный запрос возвращает id")
    def test_login_courier_success_returns_id(self):
        payload = register_new_courier_and_return_login_password()

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

    @allure.title("Авторизация с неверным полем '{wrong_field}' возвращает ошибку 404")
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_courier_wrong_credentials(self, wrong_field):
        payload = register_new_courier_and_return_login_password()

        payload[wrong_field] = "wrong_value"

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Авторизация без обязательного поля 'password' возвращает ошибку 400")
    def test_login_courier_without_required_field(self):
        payload = register_new_courier_and_return_login_password()

        del payload["login"] 

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку 404")
    def test_login_nonexistent_courier(self):
        payload = valid_courier()

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
