from django.contrib import admin
from .models import Fcuser

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', )  # 하나밖에 없어도 , 해줘야함 ',' 없으면 튜플이 아닌 문자열로 인식한다


admin.site.register(Fcuser, UserAdmin)
