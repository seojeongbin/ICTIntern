from django.shortcuts import render, redirect
# 장고내장 view연결전용 클래스 : FormView 대문자 두개 주의
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm  # 그 중에서도 회원가입, 로그인 내장폼
from django.views.generic import DetailView
from django.contrib.auth.hashers import make_password
from .models import Fcuser
from django.utils.decorators import method_decorator
from .decorators import *
from django.views.generic import View
from django.contrib import messages

# 클래스 방식의 구현
# class를 사용하는경우가 진짜 훨씬 쉽고 생산성이 좋다. 상속을 통해서 n차 이용하기도 좋고


def index(request):
    # return render(request, 'index.html') : 이건 단순히 index.html 연결해주는 기능뿐
    #
    return render(request, 'homepage.html')
    # 요렇게하면 추가로 index.html을 연결해주면서 'user'라는 키를 갖는 세션을 'email'이라는 변수 이름으로 선물하나 손에 쥐어주는거
    # index.html 가보셈 ㅇㅇ


def before(request):
    return render(request, 'index.html')

def social(request):
    return render(request, 'social.html')

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'  # success_url 이라고 이것도 내장변수임 정상적으로 들어왔을때 특정 주소로 이동할수있게해줌!! 지금은 '/'니까 홈이동 의미
# form 에 있던거 그대로 갖고와서 리팩토링 과정 (유효성 점검 부분이랑 데이터 저장부분을 나누어서 관리하는거)

    def form_valid(self, form):
        user = Fcuser(
            email=form.data.get('email'),
            password=make_password(form.data.get('password')),
        )
        user.save()

        return super().form_valid(form)


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):  # class내부에 함수추가하는데 입력받는게 self 이외에도 한개가 있다
        # form정보중에 email을 저장한다, 받고싶은 html에선 {{ email }} 하면됨
        # 여기서 user는 그냥 지정해준 거인듯 'user'라는것에 저장하겠다 이런의미인듯함
        self.request.session['user'] = form.data.get('email')
        # 자 정말 쉽게 생각하면 됨 session도 딕셔너리랑 똑같이 생각하면됨!!
        # 'user'라는 키를 만들어서 거기에 email값을 넣겠다는 것임! 그리고 id처럼 키 관리하겠단 느낌
        return super().form_valid(form)  # 저장하고 기존의 form을 반환한다
        # form_valid : 그냥 일단은 꼭 필요한거 정도라고 알아두자 지금은


def logout(request):  # 로그아웃원리는 굉장히 간단하다 . 받은 세션을 없애고 홈페이지로 빡꾸시키면 됨 ㅇㅇ
    if 'user' in request.session:
        del(request.session['user'])

    return redirect('/')  # redirect 시에는 항상 임포트 추가해주고
    # 로그아웃이거는 url에 /logout 하면 로그아웃하면서 홈으로 돌아가게 됨

# 이용약관 동의관련
#@method_decorator(logout_message_required, name='dispatch')
class AgreementView(View):
    def get(self, request, *args, **kwargs):
        request.session['agreement'] = False
        return render(request, 'agreement.html')

    def post(self, request, *args, **kwarg):
        if request.POST.get('agreement1', False) and request.POST.get('agreement2', False):
            request.session['agreement'] = True
            if request.POST.get('back') == 'back': # 뒤로가기 누른경우       
                return redirect('/')
            else: # 회원가입 버튼 누른경우
                return redirect('/register/')
        else:
            messages.info(request, "약관에 모두 동의해주세요.")
            return render(request, 'agreement.html')
'''
이용약관 로직
회원가입 버튼 Click시 회원가입(register.html)이 아닌 약관동의(agreement.html)로 redirect
url 강제입력으로 회원가입창으로 넘어가서는 안된다.
agreement.html에서 동의 checkbox가 checked되어야 /register로 redirect가 가능하다.
'''