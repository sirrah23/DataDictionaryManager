from django.test import TestCase

from .repos import ProjectRepo, DataEntryRepo
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
        desc = 'Test project'
        np = Project(description=desc)
        np.save()
        pr = ProjectRepo()
        projects = pr.get_all_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['description'], desc) 

    def test_two_projects_exist(self):
        """
        If there are multiple projects in the database then we should get their
        dictionary representations.
        """
        descs = ['Test project', 'Test project 2']
        Project(description=descs[0]).save()
        Project(description=descs[1]).save()
        pr = ProjectRepo()
        projects = pr.get_all_projects()
        self.assertEqual(len(projects), 2)
        self.assertEqual(projects[0]['description'] in descs, True) 
        self.assertEqual(projects[1]['description'] in descs, True) 
        self.assertEqual(projects[0]['id'] == projects[1]['id'] , False) 
        self.assertEqual(projects[0]['description'] == projects[1]['description'] , False) 

    def test_one_project_create(self):
        """
        Should be able to create a single project.
        """
        desc = 'Test project'
        pr = ProjectRepo()
        res = pr.create_project(desc)
        try:
            res['id']  # Key should be in dictionary
        except:
            assert False
        self.assertEqual(res['description'], desc)
        self.assertEqual(len(pr.get_all_projects()), 1)

    def test_get_one_project_by_id(self):
        """
        Should be able to get one project by its ID.
        """
        desc = 'Test Project'
        pr = ProjectRepo()
        pid = pr.create_project(desc)['id']
        res = pr.get_project_by_id(pid)
        self.assertEqual(res['description'], desc)

    def test_zero_data_entry_detail_by_project(self):
        """
        Should gracefully get zero data for a non-existent project/data entry.
        """
        dr = DataEntryRepo()
        nonexistent_project_id = 12001
        res = dr.get_entry_by_project(project_id=nonexistent_project_id)
        self.assertEqual(len(res), 0)

    def test_one_data_entry_detail_by_project(self):
        """
        Should be able to get details for a single data entry
        """
        pr = ProjectRepo()
        dr = DataEntryRepo()
        res_p = pr.create_project('Test Project')
        res_d1 = dr.create_data_entry('DE 1', res_p['id'])
        res_d2 = dr.create_data_entry('DE 2', res_p['id'])
        details = dr.get_entry_by_project(res_p['id'])
        self.assertEqual(len(details), 2)
        self.assertEqual(details[0]['id'] in [res_d1['id'], res_d2['id']], True)
        self.assertEqual(details[1]['id'] in [res_d1['id'], res_d2['id']], True)

