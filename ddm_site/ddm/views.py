from django.http import HttpResponse
from django.template import loader

from .repos import ProjectRepo


def index(request):
    project_list = ProjectRepo().get_all_projects()
    template = loader.get_template('ddm/index.html')
    context = {
            'project_list': project_list,
    }
    return HttpResponse(template.render(context))
