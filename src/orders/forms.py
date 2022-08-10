from django import forms
from .models import Order
from .utils import PHONE_NUMBER_REGEX


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label= 'Имя', widget=forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}))
    last_name = forms.CharField(label= 'Фамилия', widget=forms.TextInput(attrs={'placeholder': 'Введите вашу фамилию'}))
    email = forms.EmailField(label= 'Email', widget=forms.TextInput(attrs={'placeholder': 'Ваш почтовый адрес'}))
    phone = forms.CharField(label= 'Телефон', widget=forms.TextInput(attrs={'placeholder': 'Введите ваш номер телефона'}), validators=[PHONE_NUMBER_REGEX])
    city = forms.CharField(label= 'Город', widget=forms.TextInput(attrs={'placeholder': 'Ваш город'}))
    address = forms.CharField(label= 'Адрес', widget=forms.TextInput(attrs={'placeholder': 'Введите ваш адрес'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 'address']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mb-4'