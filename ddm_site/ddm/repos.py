from .models import Project, DataEntry, DataEntryPair


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

    def get_entry_by_id(self, dataentry_id):
        """
        Obtain the data associated with a DataEntry via the given id.
        """
        #TODO: Implement this
        pass


class DataEntryPairRepo:
    """
    A repository through which Data Entry information can be accessed.
    """

    def __init__(self):
        self.data_entry_pair_model = DataEntryPair  # TODO: Does this really provide any benefit?

    def create_data_entry_pair(self, project_id, parent_id,
                               child_id, mandatory=False,
                               optional=False, lower_limit=None,
                               upper_limit=None):
        """
        Store a data entry pair (parent+child+attributes) into the database.
        """
        dep = self.data_entry_pair_model(project_id=project_id, parent_id=parent_id,
                                         child_id=child_id, mandatory=mandatory,
                                         optional=optional, lower_limit=lower_limit,
                                         upper_limit=upper_limit)
        dep.save()

    def _build_data_entry_pair_struct(self, data):
        """
        Build a dictionary structure representing the parent-child
        relationship.
        """
        if len(data) == 0:
            return None
        r = {}

        # Initialize
        r['parent'] = {}
        r['children'] = []

        # Build
        r['project_id'] = data[0].project.id
        r['parent']['id'] = data[0].parent.id
        r['parent']['name'] = data[0].parent.name
        for item in data:
            r['children'].append({
                'id': item.child.id,
                'name': item.child.name,
                'mandatory': item.mandatory,
                'optional': item.optional,
                'lower_limit': item.lower_limit,
                'upper_limit': item.upper_limit
            })
        return r

    def get_data_entry_pairs(self, project_id, parent_id):
        """
        Get a structure representing all of the data entry pairs associated
        with the provided data entry parent.
        """
        data = self.data_entry_pair_model.objects.filter(project_id=project_id,
                                                         parent_id=parent_id)
        return self._build_data_entry_pair_struct(data)

