from django import forms
from .models import Fcuser  # models.py의 Fcuser 클래스를 이용하겠다 (밑에 회원가입할때이용)
# 비밀번호 비교기능, 비밀번호 암호기능
from django.contrib.auth.hashers import check_password, make_password


class RegisterForm(forms.Form):
    email = forms.EmailField(
        error_messages={  # 입력하지 않은경우에 대한 메세지
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호'  # 위젯은 그 비밀번호 모양 동그란 점 그거
    )
    re_password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.PasswordInput, label='비밀번호 확인'
    )

    def clean(self):  # 회원가입시 비밀번호, 비밀번호 다시 입력이 서로 틀리지않게 해주는 기능
        cleaned_data = super().clean()  # 그리고 위에서 적은 변수들을 한번 더 적어준다
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        re_password = cleaned_data.get('re_password')

        if password and re_password:
            if password != re_password:
                # 회원가입 화면 중 password부분에 비밀번호가 서로 다르다는 문구 출력
                self.add_error('password', '비밀번호가 서로 다릅니다.')
                self.add_error('re_password', '비밀번호가 서로 다릅니다.')
            ''' 리팩토링 (유효성 검사부분이랑 데이터 저장하는 부분 나누는거) else:
                fcuser = Fcuser(  # fcuser는 지금 입력받은 데이터에 대한 하나의 객체의미 & Fcuser는 입력받은걸 모델 데이터베이스로 관리하겠다는것!
                    email=email,  # 지금 입력받은 email을 데이터베이스의 email로 관리하겠단거!!
                    password=make_password(password)  # 비밀번호는 암호화로 처리!
                )
                fcuser.save()'''


class LoginForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': '이메일을 입력해주세요.'
        },
        max_length=64, label='이메일'
    )
    password = forms.CharField(
        error_messages={
            'required': '비밀번호를 입력해주세요.'
        },
        widget=forms.Textarea, label='비밀번호'
    )

    def clean(self):  # 아이디가 존재하는것이 맞고, 비밀번호가 데베 비번과 맞으면 통과하겠단것!
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                # 자 위에 객체 생성이랑 굉장히 유사하다
                # 현재 fcuser는 (위에랑 다른거긴 함) 현재 요청에 대한 새로운 객체임!
                # 근데 이거를 Fcuser 모델 클래스에 요청을 반영한 새 객체란거지!!
                user = Fcuser.objects.get(email=email)
            except Fcuser.DoesNotExist:  # 하지만 이렇게한 요청이 없는거라면 에러메세지를 처리하겠다는 것
                self.add_error('email', '아이디가 없습니다')
                return

            if not check_password(password, user.password):
                self.add_error('password', '비밀번호를 틀렸습니다')
            ''' else:
                self.email = fcuser.email  # 정상적이면 비밀번호 잘 관리하겠다 인데 이거는 그 session 처리떔에 필요한거인듯'''
