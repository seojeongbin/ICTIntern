from django.shortcuts import render
from django.http import HttpResponse
from .models import FilesAdmin

# Create your views here.


def home(request):
    context = {'file': FilesAdmin.objects.all()}
    return render(request, 'changeurl.html', context) # home -> changeurl.html


def download(request, path):  # 경로에서 갖고와서 다운기능 하게 해주는 역할
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb')as fh:
            response = HttpResponse(
                fh.read(), content_type="application/adminupload")
            response['Content-Disposition'] = 'inline;filename=' + \
                os.path.basename(file_path)
            return response

    raise Http404