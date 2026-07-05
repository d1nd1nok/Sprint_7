import allure
import requests
import pytest

from src.helpers import order_payload
from src.urls import CREATE_ORDER


class TestCreateOrder:

    @allure.title("Создание заказа с цветом {color}")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_color(self, color):
        payload = order_payload()
        payload["color"] = color

        response = requests.post(CREATE_ORDER, json=payload)

        assert response.status_code == 201
        assert "track" in response.json()
