from django.contrib import admin
from .models import Fcuser  # 이거 꼭 추가해주고

# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email', )  # 하나밖에 없어도 , 해줘야함 ',' 없으면 튜플이 아닌 문자열로 인식한다


admin.site.register(Fcuser, FcuserAdmin)  # 두 클래스를 묶어준다
