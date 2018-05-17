from django.http import HttpResponse
from django.shortcuts import render

from .repos import ProjectRepo


def index(request):
    error_message = ""
    pr = ProjectRepo()
    if request.method == 'POST':
        desc = request.POST['description']
        if not desc or len(desc) == 0: error_message = "No project description provided"
        elif not pr.create_project(desc): error_message = "Unable to create new project"
    project_list = pr.get_all_projects()
    context = {}
    context['error_message'] = error_message
    context['project_list'] = project_list
    return render(request, 'ddm/index.html', context)
