import os
import sys

import allure

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@allure.epic("Gift Helper API")
@allure.feature("Recipients Management")
class TestAPIEndpoints:

    @allure.story("Health Check")
    @allure.title("Test health check endpoint")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_health_check(self):
        with allure.step("Send GET request to /health"):
            response = client.get("/health")

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response content"):
            assert response.json() == {"status": "healthy"}

    @allure.story("Root Endpoint")
    @allure.title("Test root endpoint")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_root(self):
        with allure.step("Send GET request to /"):
            response = client.get("/")

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response message"):
            assert response.json() == {"message": "Gift Helper API"}

    @allure.story("Create Recipient")
    @allure.title("Test successful recipient creation")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_recipient_success(self):
        test_data = {"name": "Анна", "relation": "friend", "age": 25}

        with allure.step(f"Send POST request to /recipients/ with data: {test_data}"):
            response = client.post("/recipients/", json=test_data)

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response data"):
            result = response.json()

            assert result["id"] == 1
            assert result["name"] == "Анна"
            assert result["relation"] == "friend"
            assert result["age"] == 25

    @allure.story("Create Recipient")
    @allure.title("Test recipient creation without age")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_recipient_without_age(self):
        test_data = {"name": "Иван", "relation": "family"}

        with allure.step(f"Send POST request with data without age: {test_data}"):
            response = client.post("/recipients/", json=test_data)

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response data has null age"):
            result = response.json()

            assert result["id"] == 1
            assert result["name"] == "Иван"
            assert result["relation"] == "family"
            assert result["age"] is None

    @allure.story("Input Validation")
    @allure.title("Test validation error for incomplete data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_recipient_validation_error(self):
        incomplete_data = {"name": "Тест"}

        with allure.step("Send POST request with incomplete data"):
            response = client.post("/recipients/", json=incomplete_data)

        with allure.step("Verify response status code is 422 (Validation Error)"):
            assert response.status_code == 422

    @allure.story("Get Recipient")
    @allure.title("Test getting existing recipient")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_recipient_success(self):
        with allure.step("Create a recipient first"):
            create_response = client.post(
                "/recipients/", json={"name": "Олег", "relation": "brother", "age": 30}
            )
            recipient_id = create_response.json()["id"]

        with allure.step(f"Send GET request to /recipients/{recipient_id}"):
            response = client.get(f"/recipients/{recipient_id}")

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify recipient data"):
            result = response.json()
            assert result["name"] == "Олег"
            assert result["relation"] == "brother"
            assert result["age"] == 30

    @allure.story("Get Recipient")
    @allure.title("Test getting non-existent recipient")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_recipient_not_found(self):
        with allure.step("Send GET request for non-existent recipient"):
            response = client.get("/recipients/9999")

        with allure.step("Verify response status code is 404"):
            assert response.status_code == 404

        with allure.step("Verify error message"):
            assert response.json()["detail"] == "Recipient not found"

    @allure.story("List Recipients")
    @allure.title("Test getting all recipients")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_recipients(self):
        with allure.step("Create multiple recipients"):
            client.post(
                "/recipients/", json={"name": "Анна", "relation": "friend", "age": 25}
            )
            client.post(
                "/recipients/", json={"name": "Иван", "relation": "family", "age": 30}
            )

        with allure.step("Send GET request to /recipients/"):
            response = client.get("/recipients/")

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify response is a list with correct data"):
            recipients = response.json()
            assert isinstance(recipients, list)

            assert len(recipients) == 2

            for recipient in recipients:
                assert "id" in recipient
                assert "name" in recipient
                assert "relation" in recipient
                assert "age" in recipient

    @allure.story("List Recipients")
    @allure.title("Test getting empty recipients list")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_recipients_empty(self):
        with allure.step("Send GET request to /recipients/ when no recipients exist"):
            response = client.get("/recipients/")

        with allure.step("Verify response status code is 200"):
            assert response.status_code == 200

        with allure.step("Verify empty list is returned"):
            recipients = response.json()
            assert isinstance(recipients, list)

            assert len(recipients) == 0

    @allure.story("Data Isolation")
    @allure.title("Test that tests are isolated from each other")
    @allure.severity(allure.severity_level.MINOR)
    def test_data_isolation_between_tests(self):

        with allure.step("Check that repository is empty at the start of test"):
            initial_response = client.get("/recipients/")
            assert len(initial_response.json()) == 0

        with allure.step("Create one recipient"):
            response = client.post(
                "/recipients/", json={"name": "Изоляция", "relation": "test"}
            )
            assert response.status_code == 200
            assert response.json()["id"] == 1

        with allure.step("Verify only one recipient exists"):
            final_response = client.get("/recipients/")
            assert len(final_response.json()) == 1
