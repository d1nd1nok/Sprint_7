import allure
import requests
import pytest

from src.helpers import register_new_courier_and_return_login_password, valid_courier, delete_courier
from src.urls import LOGIN_COURIER
from src.messages import ACCOUNT_NOT_FOUND, NOT_ENOUGH_DATA_TO_LOGIN


class TestLoginCourier:

    @allure.title("Курьер может авторизоваться и успешный запрос возвращает id")
    def test_login_courier_success_returns_id(self):
        payload = register_new_courier_and_return_login_password()

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 200
        assert "id" in response.json()
        assert isinstance(response.json()["id"], int)

        delete_courier(payload)

    @allure.title("Авторизация с неверным полем '{wrong_field}' возвращает ошибку 404")
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_courier_wrong_credentials(self, wrong_field):
        courier = register_new_courier_and_return_login_password()

        payload = dict(courier)
        payload[wrong_field] = "wrong_value"

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND

        delete_courier(courier)

    @allure.title("Авторизация без обязательного поля 'password' возвращает ошибку 400")
    def test_login_courier_without_required_field(self):
        courier = register_new_courier_and_return_login_password()

        payload = dict(courier)
        del payload["login"]

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_TO_LOGIN

        delete_courier(courier)

    @allure.title("Авторизация под несуществующим пользователем возвращает ошибку 404")
    def test_login_nonexistent_courier(self):
        payload = valid_courier()

        response = requests.post(LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json()["message"] == ACCOUNT_NOT_FOUND
