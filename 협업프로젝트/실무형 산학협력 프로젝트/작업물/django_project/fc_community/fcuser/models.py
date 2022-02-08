from django.db import models

# Create your models here.


class Fcuser(models.Model):
    email = models.EmailField(verbose_name='이메일',null=True)
    password = models.CharField(max_length=128, verbose_name='비밀번호',null=True)
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name='등록날짜',null=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'table_user'
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
