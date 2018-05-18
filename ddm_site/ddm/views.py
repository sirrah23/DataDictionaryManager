from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

from .repos import ProjectRepo, DataEntryRepo


def index(request):
    """
    The main page of the site where the user can interact with their project list.
    """
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

def project(request, project_id):
    """
    The page to view the data entries associated with a project (and other
    project details).
    """
    # TODO: What if the project does not exist?
    pr = ProjectRepo()
    dr = DataEntryRepo()
    project = pr.get_project_by_id(project_id)
    if not project:
        return HttpResponseNotFound('Project does not exist')
    entries = dr.get_entry_by_project(project_id=project_id)
    context = {}
    context['project_desc'] = project['description']
    context['data_entries'] = entries
    return render(request, 'ddm/project.html', context)

