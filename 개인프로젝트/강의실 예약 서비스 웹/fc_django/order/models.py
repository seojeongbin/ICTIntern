from django.db import models
from product.models import Product
from fcuser.models import Fcuser
# Create your models here.


class Order(models.Model):
    fcuser = models.ForeignKey(
        'fcuser.Fcuser', on_delete=models.CASCADE, verbose_name='사용자')
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, verbose_name='상품')
    # Order의 경우 데이터베이스에서 배운거처럼 외래키로 fcuser와 product의 정보를 끌어와서 관리하겠다는 의미
    # 외래키로 작동하기위해서 ForeignKey라는 내장함수 사용하는거고, fcuser.Fcuser : fcuser 앱의 Fcuser (모델 클래스) 사용하겠다는 의미
    # 그리고 이렇게 외래키로 갖고오는경우 항상 on_delete를 설정해줘야하는데 갖고온 정보가 삭제되면 이건 어떻게 할꺼냐는 의미임 ㅇㅇ
    quantity = models.IntegerField(verbose_name='예약인원')
    # date_select = models.DateField(verbose_name='예약날짜', null=True, blank=True)
    date = models.DateTimeField(verbose_name='예약시간')
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name='등록날짜')

    def __str__(self):
        # 이런식의 문자열의 조합으로 보여주겠다는 것!
        return str(self.fcuser) + ' ' + str(self.product)

    class Meta:
        db_table = 'table_reservation'
        verbose_name = '예약'
        verbose_name_plural = '예약'
