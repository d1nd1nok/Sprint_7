import allure
import requests
import pytest

from src.helpers import valid_courier, delete_courier
from src.urls import CREATE_COURIER
from src.messages import DUPLICATE_LOGIN, NOT_ENOUGH_DATA_TO_CREATE




class TestCreateCourier:

    @allure.title("Курьер успешно создаётся с валидными данными")
    def test_create_courier_success(self):
        payload = valid_courier()
        response = requests.post(CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        delete_courier(payload)


    @allure.title("Нельзя создать двух курьеров с одинаковыми данными")
    def test_create_duplicate_courier_conflict(self):
        payload = valid_courier()

        first = requests.post(CREATE_COURIER, data=payload)
        assert first.status_code == 201

        second = requests.post(CREATE_COURIER, data=payload)
        assert second.status_code == 409
        assert second.json()["message"] == DUPLICATE_LOGIN

        delete_courier(payload)


    @allure.title("Нельзя создать курьера без обязательного поля {missing_field}")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_without_required_field(self, missing_field):
        payload = valid_courier()
        del payload[missing_field]

        response = requests.post(CREATE_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json()["message"] == NOT_ENOUGH_DATA_TO_CREATE


    @allure.title("Нельзя создать курьера с уже существующим логином")
    def test_create_courier_existing_login_conflict(self):
        first_payload = valid_courier()
        assert requests.post(CREATE_COURIER, data=first_payload).status_code == 201

        second_payload = valid_courier()
        second_payload["login"] = first_payload["login"]

        response = requests.post(CREATE_COURIER, data=second_payload)

        assert response.status_code == 409
        assert response.json()["message"] == DUPLICATE_LOGIN

        delete_courier(first_payload)

