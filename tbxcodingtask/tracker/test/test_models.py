from django.contrib.auth.models import User
from django.test import TestCase

from tbxcodingtask.tracker.factories import (
    CommentFactory,
    ProjectFactory,
    TicketFactory
)
from tbxcodingtask.tracker.models import (
    Comment,
    Project,
    Ticket
)


class TestProject(TestCase):
    def test_can_delete_project(self):
        project = ProjectFactory()
        self.assertEquals(Project.objects.all().count(), 1)
        project.delete()
        self.assertEquals(Project.objects.all().count(), 0)


class TestTicket(TestCase):
    def test_can_delete_ticket(self):
        ticket = TicketFactory()
        self.assertEquals(Ticket.objects.all().count(), 1)
        ticket.delete()
        self.assertEquals(Ticket.objects.all().count(), 0)

    def test_can_delete_ticket_when_project_is_deleted(self):
        ticket = TicketFactory()
        self.assertEquals(Project.objects.all().count(), 1)
        self.assertEquals(Ticket.objects.all().count(), 1)
        ticket.project.delete()
        self.assertEquals(Project.objects.all().count(), 0)
        self.assertEquals(Ticket.objects.all().count(), 0)


class TestComment(TestCase):
    def test_comments_are_deleted_when_ticket_is_deleted(self):
        comment = CommentFactory()
        self.assertEquals(Ticket.objects.all().count(), 1)
        self.assertEquals(Comment.objects.all().count(), 1)
        self.assertEquals(User.objects.all().count(), 1)
        comment.ticket.delete()
        self.assertEquals(Ticket.objects.all().count(), 0)
        self.assertEquals(Comment.objects.all().count(), 0)
        self.assertEquals(User.objects.all().count(), 1)

    def test_comments_are_deleted_when_author_is_deleted(self):
        comment = CommentFactory()
        self.assertEquals(Ticket.objects.all().count(), 1)
        self.assertEquals(Comment.objects.all().count(), 1)
        self.assertEquals(User.objects.all().count(), 1)
        comment.author.delete()
        self.assertEquals(Ticket.objects.all().count(), 1)
        self.assertEquals(Comment.objects.all().count(), 0)
        self.assertEquals(User.objects.all().count(), 0)

    def test_comments_and_tickets_are_deleted_when_project_is_deleted(self):
        comment = CommentFactory()
        self.assertEquals(Ticket.objects.all().count(), 1)
        self.assertEquals(Comment.objects.all().count(), 1)
        self.assertEquals(User.objects.all().count(), 1)
        comment.ticket.project.delete()
        self.assertEquals(Ticket.objects.all().count(), 0)
        self.assertEquals(Comment.objects.all().count(), 0)
        self.assertEquals(User.objects.all().count(), 1)

