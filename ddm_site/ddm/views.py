from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .repos import ProjectRepo, DataEntryRepo, DataEntryPairRepo

#TODO: Pack context-build,g data-validation, etc. into separate functions

def index(request):
    """
    The main page of the site where the user can interact with their project list.
    """
    error_message = ""
    pr = ProjectRepo()
    if request.method == 'POST':
        desc = request.POST['description']
        if not desc or len(desc) == 0:
            error_message = "No project description provided"
        elif not pr.create_project(desc):
            error_message = "Unable to create new project"
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
    context['project_id'] = project['id']
    context['project_desc'] = project['description']
    context['data_entries'] = entries
    return render(request, 'ddm/project.html', context)

def dataentry(request, project_id):
    """
    The page where the user can create a new data entry and associate it with a
    project.
    """
    error_message = ""
    if request.method == 'POST':
        dr = DataEntryRepo()
        name = request.POST['name']
        if not name or len(name) == 0:  #TODO: Check if data entry already exists
            error_message = "No Data Entry name provided"
        else:
            dr.create_data_entry(name, project_id)
            return redirect('project', project_id=project_id)
    context = {}
    context['error_message'] = error_message
    context['project_id'] = project_id
    return render(request, 'ddm/dataentry.html', context)

def dataentrypairs(request, project_id, dataentry_id):
    """
    The page where a user can create relationships between a parent and child
    data entry pair.
    """
    # Get repository objects
    pr = ProjectRepo()
    dr = DataEntryRepo()
    dpr = DataEntryPairRepo()

    if request.method == 'POST':
        mandatory = request.POST['constraint'] == 'mandatory'
        optional = request.POST['constraint'] == 'mandatory'
        dpr.create_data_entry_pair(project_id,
                                   dataentry_id,
                                   request.POST['child'],
                                   mandatory=mandatory,
                                   optional=optional,
                                   lower_limit=request.POST['lower_limit'],
                                   upper_limit=request.POST['upper_limit'])
        return redirect('dataentrypairs',
                        project_id=project_id,
                        dataentry_id=dataentry_id)

    # Pull project & data-entry data
    project = pr.get_project_by_id(project_id)
    dataentries = dr.get_entry_by_project(project_id)
    pairs = dpr.get_data_entry_pairs(project_id, dataentry_id)

    # Split dataentry list and filter
    curr_dataentry = [d for d in dataentries if d['id'] == dataentry_id][0]
    other_dataentry = [d for d in dataentries if d['id'] != dataentry_id]
    if pairs:
        other_dataentry = [d for d in other_dataentry if d['id'] not in
                           [c['id'] for c in pairs['children']]]

    # Build context for web-page
    context = {}
    context['project_id'] = project_id
    context['dataentry_id'] = dataentry_id
    context['project_desc'] = project['description']
    context['dataentry_name'] = curr_dataentry['name']
    context['dataentries'] = other_dataentry
    context['children'] = pairs['children'] if pairs else None

    return render(request, 'ddm/dataentrypairs.html', context)

