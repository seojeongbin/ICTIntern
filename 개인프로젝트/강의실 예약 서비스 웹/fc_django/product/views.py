#from fc_django.fcuser.decorators import admin_required, login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework import mixins
from fcuser.decorators import admin_required, login_required
from django.utils.decorators import method_decorator
from .models import Product
from .forms import RegisterForm
from .serializers import ProductSerializer
from django.contrib import messages
# order 의 forms.py의 레지스터폼을 불러오는데 이거를 OrderForm으로 부르겠단것(여기 product의 form과 구분해야하므로)
from order.forms import RegisterForm as OrderForm
from bootstrap_datepicker_plus import DateTimePickerInput
from django.views import generic
from .models import Product
from django.contrib import messages

# 위에 싱크로나이즈, 레스트프레임워크 두개 해서 총 세개 임포트해야함. 상속을 두개받은형태


class ProductListAPI(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ProductSerializer  # 프러덕트리스트api이건 뭐 이름주기 나름이고

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductDetailAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

# 상품을 등록하려면 로그인은 꼭 되어있어야 하고 그 유저가 admin level 이여야 한다


@method_decorator(admin_required, name='dispatch')
class ProductCreate(FormView):
    template_name = 'register_product.html'
    form_class = RegisterForm
    success_url = '/product/'

    def form_valid(self, form):
        product = Product(
            name=form.data.get('name'),
            price=form.data.get('price'),
            description=form.data.get('description'),
            stock=form.data.get('stock'),
            congestion=form.data.get('congestion')
        )
        product.save()
        return super().form_valid(form)


class ProductList(ListView):  # 리스트뷰는 장고내장형태!!
    model = Product  # 리스트뷰는 모델만 지정해주면 끝임 ~
    template_name = 'product.html'
    context_object_name = 'product_list'


# model은 models.py와 연결하기위해 있는거고, 이때 context_object_name은 편하게 사용하고자 있는부분


class ProductDetail(DetailView):  # 디테일뷰도 장고내장 형태!
    template_name = 'product_detail.html'
    queryset = Product.objects.all()  # 필터링 기능인데 all은 그냥 전체에 대해서 상세보기 기능을 제공하겠다는 것임
    # 탬플릿에서 사용할 변수명 설정. 이거 안하면 그냥 오브젝트 이런식으로 안와닿게 표현해야될것임
    # 이거땜에 다른곳에 product라고 쓰는거다!!!!!!!!!!!!!!!!!!!!!! 이건 탬플릿용이고, views.py이런데서인거는 forms.py에 product가 있는경우인거임 ㅇㅇ
    context_object_name = 'product'

    # forms.py의 내용을 탬플릿에 넘겨주는 기능임!!!! 이거 없이하면 달랑 '주문하기'버튼만 나옴. '수량'정보가 안나오고.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 그리고 이건 다른 폴더 정보내용 갖고온거 : OrderForm은 order 앱의 form 불러온거임 (위에 임포트 참고)
        context['form'] = OrderForm(self.request)
        return context

# 시간표 연결


def timetable(request):
    return render(request, 'timetable.html')


# 삭제하기 : 단순 삭제기능은 되는데, 삭제되었습니다 메세지도 이상하고, redirect도 안되고 @admin_required도 되긴하는데 메세지가 안뜸
# @admin_required  # 클래스가 아니라 함수에 적용하는경우는 이렇게
# @method_decorator(admin_required, name='dispatch')
@admin_required
def delete(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    messages.info(request, "해당 강의실이 삭제되었습니다.")
    return redirect('/product/')
    # -------- 주소(product/pk/delete/)로 하면 잘되지만, '삭제'버튼 눌러서 하는 방식의 경우 오류나고 메세지 전달도 안된다!!!!
