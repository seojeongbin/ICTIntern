from django import forms
from .models import Product


class RegisterForm(forms.Form):
    name = forms.CharField(
        error_messages={
            'required': '강의실을 입력해주세요.'
        },
        max_length=64, label='강의실 이름'
    )
    price = forms.IntegerField(
        error_messages={
            'required': '정원을 입력해주세요.'
        }, label='강의실 정원'
    )
    description = forms.CharField(
        error_messages={
            'required': '강의실 설명을 입력해주세요.'
        }, label='강의실 설명'
    )
    stock = forms.IntegerField(
        error_messages={
            'required': '예약 가능 인원을 입력해주세요.'
        }, label='예약 가능 인원'
    )
    congestion = forms.IntegerField(
        error_messages={
            'required': '강의실 혼잡도를 입력해주세요.'
        }, label='강의실 초기설정 혼잡도(%)'
    )
    # congestion = (price - stock) / stock

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        description = cleaned_data.get('description')
        stock = cleaned_data.get('stock')
        congestion = cleaned_data.get('congestion')

        if not (name and price and description and stock):
            self.add_error('name', '값이 없습니다')
            self.add_error('price', '값이 없습니다')
