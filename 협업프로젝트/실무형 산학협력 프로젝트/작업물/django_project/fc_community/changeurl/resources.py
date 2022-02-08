#from import_export import resources
from .models import Url_content

class MemberResource(resources.ModelResource):
    class Meta:
        model = Url_content
