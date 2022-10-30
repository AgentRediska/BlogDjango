from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *


class AddNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'is_published']
        labels = {
            'title': "Тема",
            'content': "Описание",
            'is_published': "Публикация"
        }
        max_lengths = {
            'title': 200,
            'content': 5000
        }
        min_lengths = {
            'title': 10,
            'content': 20
        }
        widgets = {
            'title': forms.Textarea(attrs={'style': 'width:100%;', 'cols': 80, 'rows': 2}),
            'content': forms.Textarea(attrs={'style': 'width:100%;', 'cols': 80, 'rows': 11}),
            'is_published': forms.CheckboxInput(attrs={'style': 'width:20px;height:20px;margin-left:20px;'}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'photo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 14
        self.fields['username'].help_text = "Обязательное поле. Не более 14 символов. Только буквы, цифры и символы " \
                                            "@/./+/-/_. "
        self.fields['password1'].help_text = 'Пароль не должен быть слишком похож на другую вашу личную информацию.\n' \
                                             'Ваш пароль должен содержать как минимум 8 символов.\n' \
                                             'Пароль не должен быть слишком простым и распространенным.\n' \
                                             'Пароль не может состоять только из цифр.'
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'


class CustomUserRegistrationForm(UserCreationForm):
    captcha = CaptchaField(error_messages={'invalid': 'Код неверный'})

    class Meta:
        model = User
        fields = {'username', 'photo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 14
        self.fields['username'].help_text = "Обязательное поле. Не более 14 символов. Только буквы, цифры и символы " \
                                            "@/./+/-/_. "
        self.fields['password1'].help_text = 'Пароль не должен быть слишком похож на другую вашу личную информацию.\n' \
                                             'Ваш пароль должен содержать как минимум 8 символов.\n' \
                                             'Пароль не должен быть слишком простым и распространенным.\n' \
                                             'Пароль не может состоять только из цифр.'
        self.fields['password2'].help_text = 'Для подтверждения введите, пожалуйста, пароль ещё раз.'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = {'username', 'photo'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 14
        self.fields['username'].help_text = "Не более 14 символов. Только буквы, цифры и символы @/./+/-/_."
        self.fields['password'].help_text = 'Пароли хранятся в зашифрованном виде, поэтому нет возможности посмотреть ' \
                                            'пароль.\n Чтобы изменить пароль нажмите на "Изменить пароль" '


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
