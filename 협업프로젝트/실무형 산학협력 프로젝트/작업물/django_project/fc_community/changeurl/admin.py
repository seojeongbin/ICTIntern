from django.contrib import admin
#from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import Url_content
# Register your models here.

#아마 이게 바꾼거
#class MemberResource
# @admin.register(Url_content)
# class MemberAdmin(ImportExportModelAdmin):
#     list_display = ('get_url',)
#     pass

#real
class UrlAdmin(admin.ModelAdmin):
    list_display = ('user','get_url',)
    # pass#

admin.site.register(Url_content , UrlAdmin)

#이것도 바꾼거
# admin.site.register(Url_content , MemberAdmin)