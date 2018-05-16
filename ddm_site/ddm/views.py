from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('ddm/index.html')
    return HttpResponse(template.render())
