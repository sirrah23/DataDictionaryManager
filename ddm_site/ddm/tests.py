from django.test import TestCase

from .repos import ProjectRepo, DataEntryRepo, DataEntryPairRepo
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


class DataEntryRepoTests(TestCase):

    def test_create_a_data_entry(self):
        """
        Should be able to create a valid data entry.
        """
        pr = ProjectRepo()
        dr = DataEntryRepo()
        res_p = pr.create_project('Test Project')
        res_d1 = dr.create_data_entry('DE 1', res_p['id'])
        self.assertEqual(res_d1['name'], 'DE 1')
        self.assertEqual(res_d1['project_id'], res_p['id'])

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
        Should be able to get details for all data entries associated with a
        project.
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

class DataEntryPairsRepoTests(TestCase):

    def test_one_data_entry_pair(self):
        """
        Should be able to create a single data entry pair for a given project.
        """
        pr = ProjectRepo()
        dr = DataEntryRepo()
        dpr = DataEntryPairRepo()
        res_p = pr.create_project('Test Project')
        res_d1 = dr.create_data_entry('DE 1', res_p['id'])
        res_d2 = dr.create_data_entry('DE 2', res_p['id'])
        dpr.create_data_entry_pair(res_d1['id'], res_d2['id'])
        res_dpr = dpr.get_data_entry_pairs(res_p['id'], res_d1['id'])
        self.assertEqual(res_dpr['project_id'], res_p['id'])
        self.assertEqual(res_dpr['parent']['id'], res_d1['id'])
        self.assertEqual(res_dpr['parent']['name'], res_d1['name'])
        self.assertEqual(len(res_dpr['children']), 1)
        self.assertEqual(res_dpr['children'][0]['id'], res_d2['id'])
        self.assertEqual(res_dpr['children'][0]['name'], res_d2['name'])
        self.assertEqual(res_dpr['children'][0]['mandatory'], False)
        self.assertEqual(res_dpr['children'][0]['optional'], False)
        self.assertEqual(res_dpr['children'][0]['lower_limit'], None)
        self.assertEqual(res_dpr['children'][0]['upper_limit'], None)

    def test_many_data_entry_pair(self):
        """
        Should be able to create a multiple data entry pair for a given
        project.
        """
        pr = ProjectRepo()
        dr = DataEntryRepo()
        dpr = DataEntryPairRepo()
        res_p = pr.create_project('Test Project')
        res_d1 = dr.create_data_entry('DE 1', res_p['id'])
        res_d2 = dr.create_data_entry('DE 2', res_p['id'])
        res_d3 = dr.create_data_entry('DE 3', res_p['id'])
        res_d4 = dr.create_data_entry('DE 4', res_p['id'])
        dpr.create_data_entry_pair(res_d1['id'], res_d2['id'])
        dpr.create_data_entry_pair(res_d1['id'], res_d3['id'], mandatory=True, lower_limit=5)
        dpr.create_data_entry_pair(res_d1['id'], res_d4['id'], optional=True, upper_limit=5)
        res_dpr = dpr.get_data_entry_pairs(res_p['id'], res_d1['id'])
        self.assertEqual(res_dpr['project_id'], res_p['id'])
        self.assertEqual(res_dpr['parent']['id'], res_d1['id'])
        self.assertEqual(res_dpr['parent']['name'], res_d1['name'])
        self.assertEqual(len(res_dpr['children']), 3)
        # Child 1
        self.assertEqual(res_dpr['children'][0]['id'], res_d2['id'])
        self.assertEqual(res_dpr['children'][0]['name'], res_d2['name'])
        self.assertEqual(res_dpr['children'][0]['mandatory'], False)
        self.assertEqual(res_dpr['children'][0]['optional'], False)
        self.assertEqual(res_dpr['children'][0]['lower_limit'], None)
        self.assertEqual(res_dpr['children'][0]['upper_limit'], None)
        # Child 2
        self.assertEqual(res_dpr['children'][1]['id'], res_d3['id'])
        self.assertEqual(res_dpr['children'][1]['name'], res_d3['name'])
        self.assertEqual(res_dpr['children'][1]['mandatory'], True)
        self.assertEqual(res_dpr['children'][1]['optional'], False)
        self.assertEqual(res_dpr['children'][1]['lower_limit'], 5)
        self.assertEqual(res_dpr['children'][1]['upper_limit'], None)
        # Child 3
        self.assertEqual(res_dpr['children'][2]['id'], res_d4['id'])
        self.assertEqual(res_dpr['children'][2]['name'], res_d4['name'])
        self.assertEqual(res_dpr['children'][2]['mandatory'], False)
        self.assertEqual(res_dpr['children'][2]['optional'], True)
        self.assertEqual(res_dpr['children'][2]['lower_limit'], None)
        self.assertEqual(res_dpr['children'][2]['upper_limit'], 5)
