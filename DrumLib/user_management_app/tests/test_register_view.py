import pytest
from user_management_app.views import register
from django.urls import reverse, resolve
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestRegisterView:
    def test_register_view_get(self, client):
        """
        Test the register view with a GET request:
        - Checks if the URL resolves to the correct view.
        - Ensures a 200 response status.
        - Confirms the correct template and context are used.
        """
        url = reverse('user_management_app:register')
        response = client.get(url)

        # Check the resolved function (optional, integrates the removed test)
        assert resolve(url).func == register

        # Check response and template
        assert response.status_code == 200
        assert 'user_management_app/register.html' in [t.name for t in response.templates]

        # Check if the form is passed in the context
        assert 'form' in response.context