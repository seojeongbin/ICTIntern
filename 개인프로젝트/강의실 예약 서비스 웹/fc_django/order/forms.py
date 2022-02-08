from django import forms
from .models import Order
from product.models import Product
from fcuser.models import Fcuser
from django.db import transaction


class RegisterForm(forms.Form):
    def __init__(self, request, *args, **kwargs):  # request를 form에 전달하는 기능
        super().__init__(*args, **kwargs)
        self.request = request

    quantity = forms.IntegerField(  # quantity, product는 입력값으로 받되, 사용자에 대한 정보는 세션으로 받는거니까 폼에서 추가할 필요가 없다!!
        error_messages={
            'required': '예약인원을 입력해주세요.'
        }, label='예약인원'
    )
    product = forms.IntegerField(
        error_messages={
            'required': '상품설명을 입력해주세요.'
        }, label='상품설명', widget=forms.HiddenInput  # 그 상품상세페이지에서 주문을 하는거니까 상품정보가 무엇인지에 대해서는 당연히 사용자에게 보여줄필요없다!!
    )
    date = forms.DateTimeField(
        # input_formats=['%d/%m/%Y %H:%M'],
        # widget=forms.DateTimeInput(attrs={
        #     'class': 'form-control datetimepicker-input',
        #     'data-target': '#datetimepicker1'
        # }),
        error_messages={
            'required': 'yyyy-mm-dd hh:mm 형태로 예약시간을 입력해주세요.'
        }, label='예약시간'
    )

    def clean(self):  # 주문하기를 통해 값 넘겨주면서 데이터를 저장해야 하니까
        cleaned_data = super().clean()
        quantity = cleaned_data.get('quantity')
        product = cleaned_data.get('product')
        date = cleaned_data.get('date')
        # 사용자 누군지에 대해서는 세션처리필요 ㅇㅇ
        # fuser의 view에서 정의한 세션을 여기서 활용!
        # fcuser = self.request.session.get('user')
        if not (quantity and product and date):
            self.add_error('quantity', '값이 없습니다')
            self.add_error('product', '값이 없습니다')
            self.add_error('date', '값이 없습니다')


'''        if quantity and product and fcuser:
            with transaction.atomic():  # '트랜잭션' : 일을 하나로 묶는것 (주문과, 재고감소를 하나로 묶음으로써 둘중에 하나라도 안되면 오류라고 생각함)
                prod = Product.objects.get(pk=product)
                order = Order(
                    quantity=quantity,
                    product=prod,
                    fcuser=Fcuser.objects.get(email=fcuser)
                )  # product,fcuser쓰기위해서 import 위에 주의!
                order.save()
                prod.stock -= quantity
                prod.save()

        else:
            self.product = product
            self.add_error('quantity', '값이 없습니다')
            self.add_error('product', '값이 없습니다')'''
