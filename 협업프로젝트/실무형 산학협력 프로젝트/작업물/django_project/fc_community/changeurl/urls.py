from django.urls import path
from . import views 
urlpatterns = [
    path('show/' , views.change),
    path('search/', views.search, name='api_search'),
    path('analyze/', views.data_lab , name='api_analyze'),
    path('keyword/' , views.keyword , name="keyword_crawling"), #추가

]
