import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.integration
def test_register_redirects_authenticated_user(client, user):
    client.force_login(user)
    response = client.get("/accounts/register/")
    assert response.status_code == 302

@pytest.mark.integration
def test_register_creates_user_and_logs_in(client, db):
    response = client.post("/accounts/register/", {
        "username": "newuser",
        "email": "new@example.com",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    })

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()

@pytest.mark.integration
def test_logout_redirects(client, user):
    client.force_login(user)
    response = client.get("/accounts/logout/")
    assert response.status_code == 302
