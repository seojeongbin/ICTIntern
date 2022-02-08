from django.db import models

# Create your models here.


class Fcuser(models.Model):  # 장고내부 models.Model을 상속받겠다는 의미
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=128, verbose_name='비밀번호')
    level = models.CharField(max_length=8, verbose_name='등급',
                             choices=(
                                 ('admin', 'admin'),
                                 ('user', 'user')
                             ))  # 일반 유저이냐 관리자 유저이냐 그거임
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):  # 요거는 이거 없으면 'order'에서 끌어서 쓸때 object1 이런식으로 나옴 사용자 아이디가 나오는게 아니라 ㅇㅇ
        # order가 외래키로 fcuser(앱).Fcuser(클래스) 쓰는경우 내부 변수중에 이메일을 대표로 반환하겠다는 것!
        return self.email

    class Meta:
        db_table = 'fastcampus_fcuser'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
