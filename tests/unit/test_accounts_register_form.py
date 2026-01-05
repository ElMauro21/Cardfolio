import pytest 

from accounts.forms import RegisterForm

@pytest.mark.unit
def test_register_form_valid(db):
    form = RegisterForm(data={
        "username": "newuser",
        "email": "new@example.com",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    })

    assert form.is_valid()

@pytest.mark.unit
def test_register_form_rejects_duplicate_username(db, user):
    form = RegisterForm(data={
        "username": user.username,
        "email": "other@example.com",
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    })

    assert not form.is_valid()
    assert "username" in form.errors

@pytest.mark.unit
def test_register_form_rejects_duplicate_email(db, user):
    form = RegisterForm(data={
        "username": "otheruser",
        "email": user.email,
        "password": "StrongPass123!",
        "password_confirm": "StrongPass123!",
    })

    assert not form.is_valid()
    assert "email" in form.errors

@pytest.mark.unit
def test_register_form_passwords_must_match(db):
    form = RegisterForm(data={
        "username": "user",
        "email": "user@example.com",
        "password": "StrongPass123!",
        "password_confirm": "DifferentPass123!",
    })

    assert not form.is_valid()
    assert "__all__" in form.errors
