from .models import Project


class ProjectRepo:
    """
    A repository through which project data is accessed.
    """

    def __init__(self):
        self.project_model = Project

    def _project_to_dict(self, p):
        """
        Convert a project object to a dictionary.
        """
        r = {}
        r["id"] = p.id
        r["description"] = p.description
        return r

    def get_all_projects(self):
        """
        Get all projects in the database.
        """
        data = self.project_model.objects.all()
        return list(map(self._project_to_dict, data))

    def create_project(self, desc):
        """
        Create a project given its description
        """
        p = self.project_model(description=desc)
        p.save()
        return self._project_to_dict(p)

