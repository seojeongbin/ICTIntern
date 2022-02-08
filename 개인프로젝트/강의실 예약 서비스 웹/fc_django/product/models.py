from django.db import models
# Create your models here.


class Product(models.Model):  # 유저에 대한 정보는 외래키로 받지 않았음. 상품 생성시의 사람은 외부 공급자이고 주문하는 사람과 다르니까
    name = models.CharField(
        max_length=256, verbose_name='상품명', null=True)
    price = models.IntegerField(verbose_name='상품가격', null=True)
    description = models.TextField(verbose_name='상품설명', null=True)
    stock = models.IntegerField(verbose_name='재고', null=True)
    congestion = models.IntegerField(
        verbose_name='강의실 혼잡도', null=True)
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name='등록날짜', null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fastcampus_product'  # 이거 mysql 연동 후 이름바꾸면 안됨!!!!
        verbose_name = '상품'
        verbose_name_plural = '상품'
