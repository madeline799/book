from django import forms
from django.forms.widgets import PasswordInput


class RegisterForm(forms.Form):

    """Form for user registration."""

    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=PasswordInput, min_length=5)
    password2 = forms.CharField(widget=PasswordInput)
    email = forms.EmailField(max_length=75)
    name = forms.CharField(max_length=100)

    def clean(self):
        """Check whether the two passwords match."""
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self._errors["password2"] = self.error_class([
                u'Passwords not match.',
                ])
            del cleaned_data["password2"]
        return cleaned_data


class LoginForm(forms.Form):

    """Form for user login."""

    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=PasswordInput)
