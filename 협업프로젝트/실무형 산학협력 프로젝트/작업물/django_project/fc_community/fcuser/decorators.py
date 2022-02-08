from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Fcuser
from django.contrib import messages

# 데코레이터란? : 함수를 포함하는 함수개념!
# 권한설정에 주로 쓰임 : 로그인안하고 주문하려고하면 로그인창으로 돌려보냄


def login_required(function):
    def wrap(request, *args, **kwargs):  # 여기서 인자는 사용하고자 하는 함수(dispatch)랑 인자 개수 맞춰줘야 함
        user = request.session.get('user')
        # if user is None or not user:  # None이거나 비어있으면 로그인창으로 돌려보냄
        if not request.user.is_authenticated: # 이거 임포트 없이 쓸수있는 장고기능        
            messages.info(request, "로그인한 사용자만 이용할 수 있습니다.") # 알림문구 없어도 작동가능 당연 ㅇㅇ
            return redirect('/login')
        return function(request, *args, **kwargs)

    return wrap

# 요건 제품을 등록하려고하면 로그인한 유저가 admin레벨이 아니라면 홈페이지로 돌려보냄


def admin_required(function):
    def wrap(request, *args, **kwargs):
        user = request.session.get('user')
        if user is None or not user:
            return redirect('/login')

        user = Fcuser.objects.get(email=user)
        if user.level != 'admin':
            messages.info(request, "접근 권한이 없습니다.")
            return redirect('/')

        return function(request, *args, **kwargs)

    return wrap

# 마지막으로 이건 이미 로그인한 사용자의 회원가입, 로그인을 막기 위함
def logout_message_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "접속중인 사용자입니다.")
            return redirect('/users/main/')
        return function(request, *args, **kwargs)
    return wrap