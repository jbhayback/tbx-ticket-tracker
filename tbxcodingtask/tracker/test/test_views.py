from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from tbxcodingtask.tracker.models import (
    Comment,
    Project,
    Ticket
)


class TestProjectListView(TestCase):
    def setUp(self):
        self.client = Client()
        Project.objects.create(title="Test")
        Project.objects.create(title="Test2")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/project_list.html')
    
    def test_view_lists_all_projects(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['project_list']), 2)


class TestCreateProjectView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/projects/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get('/projects/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/project_form.html')
    
    def test_create_project_successfully(self):
        self.assertEquals(Project.objects.all().count(), 0)
        response = self.client.post('/projects/create/', data={"title": "New Project"})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Project.objects.all().count(), 1)
        project = Project.objects.get(title="New Project")
        self.assertEqual(project.title, "New Project")


class TestUpdateProjectView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)

    def test_view_url_exists_at_desired_location(self):
        project = Project.objects.create(title="Test")
        response = self.client.get(f'/projects/{project.pk}/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        project = Project.objects.create(title="Test")
        response = self.client.get(f'/projects/{project.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/project_detail.html')
    
    def test_update_project_successfully(self):
        project = Project.objects.create(title="Test")
        self.assertEqual(project.title, "Test")
        response = self.client.post(f'/projects/{project.pk}/edit/', data={"title": "New Title"})
        self.assertEqual(response.status_code, 302)
        project.refresh_from_db()
        self.assertEqual(project.title, "New Title")
    

class TestDeleteProjectView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)
        self.project = Project.objects.create(title="Test")
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/projects/{self.project.pk}/delete/')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(f'/projects/{self.project.pk}/delete/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/confirm_delete.html')
    
    def test_delete_project_successfully(self):
        self.assertEquals(Project.objects.all().count(), 1)
        response = self.client.post(f'/projects/{self.project.pk}/delete/', data={"title": "Test"})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Project.objects.all().count(), 0)


class TestProjectView(TestCase):
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(title="Test")
        Ticket.objects.create(title="Test Ticket", project_id=self.project.pk)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/projects/{self.project.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(f'/projects/{self.project.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/project_detail.html')
    
    def test_view_project_details(self):
        response = self.client.get(f'/projects/{self.project.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'].title, "Test")
        self.assertEqual(len(response.context['tickets']), 1)


class TestCreateTicketView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        self.project = Project.objects.create(title="Test")
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/create')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/create')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/ticket_form.html')
    
    def test_create_ticket_successfully(self):
        self.assertEquals(Ticket.objects.all().count(), 0)
        response = self.client.post(f'/projects/{self.project.pk}/tickets/create', data={"title": "Test"})
        self.assertEqual(response.status_code, 302)
        self.assertEquals(Ticket.objects.all().count(), 1)


class TestUpdateTicketView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        self.project = Project.objects.create(title="Test")
        self.ticket = Ticket.objects.create(title="Test Ticket", project_id=self.project.pk)
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}/edit')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/ticket_form.html')

    def test_update_ticket_successfully(self):
        self.assertEqual(self.ticket.title, "Test Ticket")
        response = self.client.post(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}/edit', data={"title": "New Ticket Title"})
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.title, "New Ticket Title")


class TestDeleteTicketView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        self.project = Project.objects.create(title="Test")
        self.ticket = Ticket.objects.create(title="Test Ticket", project_id=self.project.pk)
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}/delete')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}/delete')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/confirm_delete.html')

    def test_delete_ticket_successfully(self):
        self.assertEquals(Project.objects.all().count(), 1)
        self.assertEquals(Ticket.objects.all().count(), 1)
        response = self.client.post(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}/delete', data={"title": "New Ticket Title"})
        self.assertEqual(response.status_code, 302)
        self.project.refresh_from_db()
        self.assertEquals(Project.objects.all().count(), 1)
        self.assertEquals(Ticket.objects.all().count(), 0)


class TicketDetailView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', password="test1234")
        self.project = Project.objects.create(title="Test")
        self.ticket = Ticket.objects.create(title="Test Ticket", project_id=self.project.pk)
        resp = self.client.post('/accounts/login/', {'username': 'test_user', 'password': 'test1234'})
        self.assertEqual(resp.status_code, 302)
    
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}')
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracker/ticket_detail.html')
        
    def test_view_gets_ticket_details_successfully(self):
        comment_1 = Comment.objects.create(author=self.user, ticket=self.ticket, content=['Test comment'])
        comment_2 = Comment.objects.create(author=self.user, ticket=self.ticket, content=['Test comment 2'])
        self.ticket.refresh_from_db()
        response = self.client.get(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['ticket'].title, "Test Ticket")
        self.assertEquals(len(response.context['ticket'].comments.all()), 2)
        self.assertEquals(response.context['ticket'].comments.all()[0].content, "['Test comment']")
        self.assertEquals(response.context['ticket'].comments.all()[1].content, "['Test comment 2']")

    def test_view_adds_new_comment_to_ticket_successfully(self):
        comment_1 = Comment.objects.create(author=self.user, ticket=self.ticket, content=['Test comment'])
        response = self.client.post(f'/projects/{self.project.pk}/tickets/{self.ticket.pk}', data={"content":"['New Comment']"})
        self.ticket.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['ticket'].title, "Test Ticket")
        self.assertEquals(len(response.context['ticket'].comments.all()), 2)
        self.assertEquals(response.context['ticket'].comments.all()[0].content, "['Test comment']")
        self.assertEquals(response.context['ticket'].comments.all()[1].content, "['New Comment']")
