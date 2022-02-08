from django.contrib import admin
from django.urls import path, include
# fcuser의 views.py에서 만든 index, Registerview 와 연결하기위함
from fcuser.views import index, RegisterView, RegisterViewForAdmin, LoginView, logout
from product.views import ProductList, ProductCreate, ProductDetail, ProductListAPI, ProductDetailAPI, timetable, delete
from order.views import OrderCreate, OrderList, OrderListAll
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),  # ''공백으로 아무것도 주지않음으로써 홈페이지로 쓴단거
    # 함수가 아니라 클래스를 갖고오는거라면 .as_view() 써줘야함!
    path('logout/', logout),
    path('register/', RegisterView.as_view()),
    path('registerforadmin/', RegisterViewForAdmin.as_view()),
    path('login/', LoginView.as_view()),
    path('product/', ProductList.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    path('product/create/', ProductCreate.as_view()),
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),
    path('orderAll/', OrderListAll.as_view()),
    path('api/product/', ProductListAPI.as_view()),
    path('api/product/<int:pk>/', ProductDetailAPI.as_view()),
    path('timetable/', timetable),
    path('product/<int:pk>/delete/', delete),
    path('users/', include('fcuser.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
