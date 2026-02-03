import pytest
from django.conf import settings

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    """Настройка тестовой БД один раз для всех тестов"""
    pass

@pytest.fixture
def api_client():
    """DRF API клиент для тестов"""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def admin_user(db):
    """Создать админ-пользователя"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='testpass123'
    )

@pytest.fixture
def user(db):
    """Создать обычного пользователя"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='testpass123'
    )

@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Автоматически включать доступ к БД для всех тестов"""
    pass

@pytest.fixture
def client():
    """Django test client для тестирования views"""
    from django.test import Client
    return Client()

