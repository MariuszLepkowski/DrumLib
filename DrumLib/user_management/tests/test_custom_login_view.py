import pytest
from django.urls import resolve, reverse
from user_management_app.views import CustomLoginView


@pytest.mark.login_tests
@pytest.mark.django_db
class TestCustomLoginView:
    def test_custom_login_view_get(self, client):
        """
        Test the CustomLoginView  with a GET request:
        - Checks if the URL resolves to the correct view.
        - Ensures a 200 response status.
        - Confirms the correct template and context are used.
        """

        url = reverse("user_management_app:login")
        response = client.get(url)

        # Check if URL resolves to the correct view class
        assert issubclass(resolve(url).func.view_class, CustomLoginView)

        # Check response and template
        assert response.status_code == 200
        assert "user_management_app/login.html" in [t.name for t in response.templates]

        # Check if the form is passed in the context
        assert "form" in response.context
