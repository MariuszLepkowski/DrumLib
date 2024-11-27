import pytest
from user_management_app.views import logout_view
from django.urls import reverse, resolve


class TestLogoutView:
    def test_logout_view_url(self):
        path = reverse('user_management_app:logout')
        assert resolve(path).func == logout_view