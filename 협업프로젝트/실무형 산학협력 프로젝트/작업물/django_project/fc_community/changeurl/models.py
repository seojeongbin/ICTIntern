from django.db import models
from fcuser.models import Fcuser

# Create your models here.


class Url_content(models.Model):
    #문제 해결됨 --> 즉 외래키가 널값이 들어갈수 있으면 테이블에 넣을수 있다는건가
    #근데 나타나는 곳에서 사용자 네임이 하나로 특정되지 않네....
    #view 에서 changeurl 클래스에서 save 해줄때 사용자 id 세션 값을 넘겨주면 되겠다 6시 29분
    #
    user = models.ForeignKey('fcuser.Fcuser' , on_delete = models.CASCADE , verbose_name ='사용자' , null=True)
    #지금 url 만 널값 참으로 만듬
    #null = True
    get_url = models.URLField(verbose_name= "url 값" ,null = True)
    input_image = models.ImageField(null = True)
    CHOICES = (
    ('naver','NAVER'),
    ('g-market', 'G-MARKET'),
    ('coupang','COUPANG'),
)
    site = models.CharField(max_length=12, choices=CHOICES, default='naver')
    registered_dttm = models.DateTimeField(auto_now=True, verbose_name='등록시간', null = True)


    def __str__(self):
        return 'user={0}, url={1}'.format(self.user, self.get_url)
        

class Meta:
    db_table = "changeUrl_url"
    verbose_name ='url 값'
    verbose_name_plural = "url 값"