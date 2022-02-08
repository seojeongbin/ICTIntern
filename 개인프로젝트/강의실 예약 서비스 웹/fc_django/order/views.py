from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic import ListView
# from django.utils.decorators import method_decorator
# from fcuser.decorators import login_required
from django.db import transaction
from .forms import RegisterForm
from .models import Order
from .models import Product
from .models import Fcuser
# 클래스방식에서 데코레이터를 쓰는경우 이거를 임포트해줘야함!
from fcuser.decorators import *
from django.utils.decorators import method_decorator
from django.contrib import messages

# Create your views here.
# dispatch라는 함수와 login_required라는 데코레이터 함수를 연결해주는 ㅇㅇ


@method_decorator(login_required, name='dispatch')
class OrderCreate(FormView):  # 페이지 보여주는 용도가 아니므로 탬플릿 지정은 해줄필요 없음
    # 이거 아마 그래서 url에 직접 /order/create/하면 오류나는듯..???
    form_class = RegisterForm  # 이거 forms.py 에서 정의한거
    success_url = '/product/'  # 하지만 성공하면 다시 상품목록으로 바뀌도록 ㅇㅇ
    # 리팩토링 위해 form의 데이터 저장부분을 여기로 들고옴

    def form_valid(self, form):
        with transaction.atomic():
            working = True
            prod = Product.objects.get(pk=form.data.get('product'))
            if float(prod.congestion) >= 100:
                working = False
                messages.info(self.request, '예약이 불가능합니다.')
            if working:
                # 어떻게 그전꺼를 그대로 이어오냐인데 이거는 forms.py로 product연결한단거!!!!!
                # prod = Product.objects.get(pk=form.data.get('product'))
                order = Order(
                    quantity=form.data.get('quantity'),
                    date=form.data.get('date'),
                    product=prod,
                    fcuser=Fcuser.objects.get(
                        email=self.request.session.get('user')),  # 세션처리로 유저 정보 받아온다!!!!
                )
                order.save()
            ###### 주문을 함으로써 일어나는 현상이기 때문에 product가 아닌 여기에서 적용해주는듯!! ##########
            ###### 그렇기때문에 혼잡도 부분도 예약을 잡으면서 일어나는거라서 이렇게 여기다가 넣어줌 ########
                prod.stock -= int(form.data.get('quantity'))
                prod.congestion += float(int(form.data.get('quantity')
                                             ) / int(prod.price))*100
                # congestion이 form 생성시 기존에 원래 있는값이라 그냥 정의로는 안되고 있는값에서 변경해주는식으로 +=, -= 이렇게 해줘야하는듯!!!!!!!!! 기모찌!!!
                prod.save()
        return super().form_valid(form)

    def form_invalid(self, form):  # 오류일때(로그인안한 상태에서 한다거나) 어느페이지에 에러를 던져야 할지 모르겠단 이슈가 있으므로
        # 오류날경우 redirect시킴. 즉 잘못된 정보면 안받고 상품목록 페이지로 빡꾸 시킨다거임 (상세 목록 페이지인듯)
        return redirect('/product/' + str(form.data.get('product')))

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw


# 개인별 주문 목록 보기 (강의실별 보기도 좋을듯?)
@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    template_name = 'order.html'
    context_object_name = 'order_list'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.filter(
            fcuser__email=self.request.session.get('user'))
        return queryset


# 전체 주문 목록 보기
class OrderListAll(ListView):
    template_name = 'orderAll.html'
    context_object_name = 'order_list_All'

    def get_queryset(self, **kwargs):
        queryset = Order.objects.all()
        return queryset
