from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code="inactive")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                if not User.objects.filter(username=username).exists():
                    raise forms.ValidationError(
                        "The user does not exist.", code="invalid_login"
                    )
                else:
                    raise forms.ValidationError(
                        "Invalid password. Try again.", code="invalid_login"
                    )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional")
    personal_info = forms.CharField(
        widget=forms.Textarea, required=False, help_text="Optional"
    )
    avatar = forms.ImageField(required=False, help_text="Optional")

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "personal_info", "avatar"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        user = self.instance.user

        self.fields["first_name"].initial = self.instance.user.first_name
        self.fields["first_name"].widget.attrs["placeholder"] = user.first_name
        self.fields["last_name"].initial = self.instance.user.last_name
        self.fields["last_name"].widget.attrs["placeholder"] = user.last_name
        self.fields["personal_info"].widget.attrs[
            "placeholder"
        ] = "Tell us about yourself"  # Example placeholder
