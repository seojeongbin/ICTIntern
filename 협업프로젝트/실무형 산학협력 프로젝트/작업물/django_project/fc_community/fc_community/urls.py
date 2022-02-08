from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from fcuser.views import index, RegisterView, LoginView, logout, social , before
from django.conf.urls import url
from blog.views import home
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('before/' , before),
    # path('before , before')  # ''공백으로 아무것도 주지않음으로써 홈페이지로 쓴단거
    # 함수가 아니라 클래스를 갖고오는거라면 .as_view() 써줘야함!
    path('social/', social),
    path('register/', RegisterView.as_view()),
    path('changeurl/',include('changeurl.urls')),
    path('login/', LoginView.as_view()),
    path('logout/', logout),
    url(r'^download/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    path('result/', home),
    path('users/', include('fcuser.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)