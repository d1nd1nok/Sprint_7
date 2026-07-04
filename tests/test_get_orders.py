import allure
import requests

from src.urls import GET_ORDERS


class TestGetOrders:

    @allure.title("В теле ответа возвращается список заказов")
    def test_get_orders_returns_list(self):
        response = requests.get(GET_ORDERS)

        assert response.status_code == 200
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Запрос с несуществующим courierId возвращает 404")
    def test_get_orders_nonexistent_courier(self):
        courier_id = 999999999

        response = requests.get(GET_ORDERS, params={"courierId": courier_id})

        assert response.status_code == 404
        assert response.json()["message"] == f"Курьер с идентификатором {courier_id} не найден"
