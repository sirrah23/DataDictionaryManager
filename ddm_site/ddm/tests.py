from django.test import TestCase

from .repos import ProjectRepo
from .models import Project

class ProjectRepoTests(TestCase):

    def test_no_projects_exist(self):
        """
        If there are no projects in the database then we will return None.
        """
        pr = ProjectRepo()
        self.assertEqual(len(pr.get_all_projects()), 0)

    def test_one_project_exists(self):
        """
        If there is one project in the database we should get it's dictionary
        representation.
        """
        desc = "Test project"
        np = Project(description=desc)
        np.save()
        pr = ProjectRepo()
        projects = pr.get_all_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["description"], desc) 

    def test_two_projects_exist(self):
        """
        If there are multiple projects in the database then we should get their
        dictionary representations.
        """
        descs = ["Test project", "Test project 2"]
        Project(description=descs[0]).save()
        Project(description=descs[1]).save()
        pr = ProjectRepo()
        projects = pr.get_all_projects()
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0]["description"] in descs, True) 
        self.assertEqual(projects[1]["description"] in descs, True) 
        self.assertEqual(projects[0]["id"] == projects[1]["id"] , False) 
        self.assertEqual(projects[0]["description"] == projects[1]["description"] , False) 

