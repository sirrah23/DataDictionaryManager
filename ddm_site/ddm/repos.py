from .models import Project, DataEntry


class ProjectRepo:
    """
    A repository through which project data is accessed.
    """

    def __init__(self):
        self.project_model = Project  # TODO: Does this really provide any benefit?

    def _to_dict(self, p):
        """
        Convert a project object to a dictionary.
        """
        r = {}
        r["id"] = p.id
        r["description"] = p.description
        return r

    def get_project_by_id(self, project_id):
        """
        Get a project via its ID.
        """
        p = self.project_model.objects.filter(id=project_id)
        return self._to_dict(p[0]) if len(p) > 0 else None

    def get_all_projects(self):
        """
        Get all projects in the database.
        """
        data = self.project_model.objects.all()
        return list(map(self._to_dict, data))

    def create_project(self, desc):
        """
        Create a project given its description
        """
        p = self.project_model(description=desc)
        p.save()
        return self._to_dict(p)


class DataEntryRepo:
    """
    A repository through which Data Entry information can be accessed.
    """
    def __init__(self):
        self.data_entry_model = DataEntry  # TODO: Does this really provide any benefit?

    def _to_dict(self, de):
        """
        Convert a DataEntry object to a dictionary.
        """
        r = {}
        r["id"] = de.id
        r["name"] = de.name
        r["project_id"] = de.project_id
        return r

    def create_data_entry(self, name, project_id):
        """
        Create a row in the Data Entry table associated with the given
        project.
        """
        de = self.data_entry_model(name=name, project_id=project_id)
        de.save()
        return self._to_dict(de)

    def get_entry_by_project(self, project_id):
        """
        Get all data entries associated with the input project.
        """
        return list(
            map(lambda d: self._to_dict(d),
                self.data_entry_model.objects.filter(project_id=project_id)))
