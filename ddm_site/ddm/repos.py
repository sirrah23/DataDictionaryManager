from .models import Project


class ProjectRepo:
    """
    A repository through which project data is accessed.
    """

    def __init__(self):
        self.project_model = Project

    def _project_to_dict(self, p):
        r = {}
        r["id"] = p.id
        r["description"] = p.description
        return r

    def get_all_projects(self):
        data = self.project_model.objects.all()
        return list(map(self._project_to_dict, data))

