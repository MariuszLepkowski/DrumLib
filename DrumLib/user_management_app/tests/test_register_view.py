import pytest
from user_management_app.views import register
from django.urls import reverse, resolve


class TestRegisterView:
    def test_register_view_url(self):
        path = reverse('user_management_app:register')
        assert resolve(path).func == register