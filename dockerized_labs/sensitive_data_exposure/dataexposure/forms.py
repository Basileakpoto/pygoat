from django import forms
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2']


class UserDataForm(forms.Form):
    credit_card = forms.CharField(
        label="Numéro de carte fictif",
        max_length=16,
        min_length=16
    )
        
    ssn = forms.CharField(
        label="Identifiant fictif",
        max_length=9,
        min_length=9
    )
    def clean_ssn(self):
        ssn = self.cleaned_data["ssn"]
        if not ssn.isdigit():
            raise forms.ValidationError(
                "L'identifiant fictif doit contenir exactement 9 chiffres."
            )
        return ssn
    def clean_credit_card(self):
                credit_card = self.cleaned_data["credit_card"]
                if not credit_card.isdigit():
                    raise forms.ValidationError(
                        "Le numéro de carte fictif doit contenir exactement 16 chiffres."
                    )
                return credit_card